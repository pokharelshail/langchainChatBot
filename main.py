import os
import json
from dotenv import load_dotenv
from langchain.schema import HumanMessage, SystemMessage
from langchain_community.callbacks import get_openai_callback


# Load environment variables
load_dotenv()


def get_data_source():
    """Load and return the path to the local JSON data source"""
    data_file = "data_source.json"
    if not os.path.exists(data_file):
        raise FileNotFoundError(f"{data_file} not found. Please run pre_process.py to fetch data.")
    return data_file

def setup_chat_model(provider="google"):
    """Setup chat model based on provider choice"""
    
    data_file = get_data_source()
    with open(data_file, 'r') as f:
        data_source = json.load(f)
    
    # Convert data to string for system prompt
    data_string = json.dumps(data_source, indent=2)
    
    SYSTEM_PROMPT = (f"You are a helpful assistant that provides information about Data Source. "
                   f"Use the provided data to answer questions accurately. "
                   f"If the information is not available, respond with 'I don't know'.\n\n"
                   f"Data:\n{data_string}")

    print(f"Loaded {len(data_source)} items for the assistant.")
    if provider.lower() == "google":
        from langchain_google_genai import ChatGoogleGenerativeAI
        chat_model = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=os.getenv("GOOGLE_API_KEY"),
            temperature=0.7
        )
        return chat_model, SYSTEM_PROMPT
    
    elif provider.lower() == "openai":
        from langchain_openai import ChatOpenAI
        chat_model = ChatOpenAI(
            model="gpt-3.5-turbo",
            api_key=os.getenv("OPENAI_API_KEY"),
            temperature=0.7
        )
        return chat_model, SYSTEM_PROMPT
    
    else:
        raise ValueError("Provider must be 'google' or 'openai'")

def chatbot():
    # Choose your provider here
    provider = input("Choose provider (google/openai): ").strip().lower()
    
    try:
        chat, system_prompt = setup_chat_model(provider)
        print(f"{provider.title()} Chatbot started! Type 'quit' to exit.")
        
        while True:
            user_input = input("\nYou: ")
            
            if user_input.lower() == 'quit':
                print("Goodbye!")
                break
            
            try:
                # Create messages with system prompt and user input
                messages = [
                    SystemMessage(content=system_prompt),
                    HumanMessage(content=user_input)
                ]
                
                # Use LangChain's token tracking callback
                if provider.lower() == "openai":
                    with get_openai_callback() as cb:
                        response = chat.invoke(messages)
                        print(f"Bot: {response.content}")
                        print(f"\n📊 Token Usage:")
                        print(f"   Prompt tokens: {cb.prompt_tokens:,}")
                        print(f"   Completion tokens: {cb.completion_tokens:,}")
                        print(f"   Total tokens: {cb.total_tokens:,}")
                        print(f"   Total cost: ${cb.total_cost:.6f}")
                else:
                    # For non-OpenAI providers, LangChain doesn't have built-in token tracking
                    # But we can still get the response
                    response = chat.invoke(messages)
                    print(f"Bot: {response.content}")
                    
                    # Check if response has usage_metadata (newer LangChain versions)
                    if hasattr(response, 'usage_metadata') and response.usage_metadata:
                        usage = response.usage_metadata
                        print(f"\n📊 Token Usage:")
                        print(f"   Input tokens: {usage.get('input_tokens', 'N/A'):,}")
                        print(f"   Output tokens: {usage.get('output_tokens', 'N/A'):,}")
                        print(f"   Total tokens: {usage.get('total_tokens', 'N/A'):,}")
                    else:
                        print(f"\n📊 Token usage not available for {provider} provider")
                
            except Exception as e:
                print(f"Error: {e}")
                
    except Exception as e:
        print(f"Setup error: {e}")

if __name__ == "__main__":
    chatbot()