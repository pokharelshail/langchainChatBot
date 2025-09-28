import os
from dotenv import load_dotenv
from langchain.schema import HumanMessage

# Load environment variables
load_dotenv()

def setup_chat_model(provider="google"):
    """Setup chat model based on provider choice"""
    
    if provider.lower() == "google":
        from langchain_google_genai import ChatGoogleGenerativeAI
        return ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=os.getenv("GOOGLE_API_KEY"),
            temperature=0.7
        )
    
    elif provider.lower() == "openai":
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(
            model="gpt-3.5-turbo",
            api_key=os.getenv("OPENAI_API_KEY"),
            temperature=0.7
        )
    
    else:
        raise ValueError("Provider must be 'google' or 'openai'")

def chatbot():
    # Choose your provider here
    provider = input("Choose provider (google/openai): ").strip().lower()
    
    try:
        chat = setup_chat_model(provider)
        print(f"{provider.title()} Chatbot started! Type 'quit' to exit.")
        
        while True:
            user_input = input("\nYou: ")
            
            if user_input.lower() == 'quit':
                print("Goodbye!")
                break
            
            try:
                response = chat.invoke([HumanMessage(content=user_input)])
                print(f"Bot: {response.content}")
                
            except Exception as e:
                print(f"Error: {e}")
                
    except Exception as e:
        print(f"Setup error: {e}")

if __name__ == "__main__":
    chatbot()