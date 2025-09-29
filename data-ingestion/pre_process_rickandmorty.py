import json
import requests
from typing import List, Dict, Any

def fetch_character(character_id: int) -> Dict[str, Any]:
    """Fetch character data from Rick & Morty API"""
    try:
        response = requests.get(f"https://rickandmortyapi.com/api/character/{character_id}")
        return response.json() if response.status_code == 200 else None
    except:
        return None

def extract_episode_ids(episode_urls: List[str]) -> List[int]:
    """Extract episode IDs from URLs"""
    return [int(url.split('/')[-1]) for url in episode_urls]

def extract_location_info(location_data: Dict) -> Dict:
    """Extract location ID and name"""
    if not location_data or not location_data.get('url'):
        return {"id": None, "name": location_data.get('name', 'Unknown')}
    
    location_id = location_data['url'].split('/')[-1] if location_data['url'] else None
    return {
        "id": int(location_id) if location_id and location_id.isdigit() else None,
        "name": location_data.get('name', 'Unknown')
    }

def map_character_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Map character data for LLM consumption"""
    if not data:
        return None
    
    # Extract episode IDs for easier querying
    episode_ids = extract_episode_ids(data.get('episode', []))
    
    # Extract location info
    origin_info = extract_location_info(data.get('origin', {}))
    location_info = extract_location_info(data.get('location', {}))
    
    mapped_data = {
        # Basic character info
        "id": data["id"],
        "name": data["name"],
        "status": data["status"],  # Alive, Dead, unknown
        "species": data["species"],  # Human, Alien, etc.
        "type": data.get("type", ""),  # Subspecies info
        "gender": data["gender"],
        
        # Location data (structured for LLM)
        "origin": origin_info,
        "current_location": location_info,
        
        # Episode appearances
        "episode_count": len(episode_ids),
        "episode_ids": episode_ids,
        "first_appearance": min(episode_ids) if episode_ids else None,
        "last_appearance": max(episode_ids) if episode_ids else None,
        
        # Additional metadata
        "image_url": data.get("image"),
        "api_url": data.get("url"),
        "created_date": data.get("created"),
        
        # LLM-friendly summary
        "description": f"{data['name']} is a {data['status'].lower()} {data['species'].lower()} " +
                      f"({data['gender'].lower()}) who originated from {origin_info['name']} " +
                      f"and currently resides in {location_info['name']}. " +
                      f"Appeared in {len(episode_ids)} episodes.",
        
        # Search/filter friendly fields
        "searchable_text": f"{data['name']} {data['species']} {data['status']} {data['gender']} " +
                           f"{origin_info['name']} {location_info['name']} {data.get('type', '')}"
    }
    
    return mapped_data

def process_characters(start_id: int, end_id: int, filename: str = "characters_processed.json"):
    """Process character data for LLM use"""
    all_character_data = []
    
    for character_id in range(start_id, end_id + 1):
        print(f"Processing character {character_id}...")
        data = fetch_character(character_id)
        
        if data:
            mapped_data = map_character_data(data)
            if mapped_data:
                all_character_data.append(mapped_data)
    
    # Save processed data
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(all_character_data, f, indent=2, ensure_ascii=False)
    
    print(f"Saved {len(all_character_data)} characters to {filename}")
    return all_character_data

# Example usage
if __name__ == "__main__":
    # Process first 20 characters
    characters = process_characters(1, 20)
    
    # Print example of processed data
    if characters:
        print("\nExample processed character:")
        print(json.dumps(characters[0], indent=2))