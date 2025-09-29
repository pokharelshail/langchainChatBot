import json

# Download and add to JSON file from 1 - 100 pokemons from pokeapi.com
import requests

def fetch_data(pokemon_id):
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch data for Pokemon ID {pokemon_id}")
        return None

def fetch_and_save_pokemon_data(start_id, end_id, filename="pokemon_data.json"):
    all_pokemon_data = []
    for pokemon_id in range(start_id, end_id + 1):
        data = fetch_data(pokemon_id)
        if data:
            # Map data to relevant chunks
            mapped_data = {
                "id": data["id"],
                "name": data["name"],
                "height": data["height"],
                "weight": data["weight"],
                "base_experience": data["base_experience"],
                "types": [type_info["type"]["name"] for type_info in data["types"]],
                "abilities": [ability["ability"]["name"] for ability in data["abilities"]],
                "stats": {stat["stat"]["name"]: stat["base_stat"] for stat in data["stats"]},
                # "sprites": {
                #     "front_default": data["sprites"]["front_default"],
                #     "front_shiny": data["sprites"]["front_shiny"],
                #     "official_artwork": data["sprites"]["other"]["official-artwork"]["front_default"] if data["sprites"]["other"]["official-artwork"]["front_default"] else None
                # }
            }
            all_pokemon_data.append(mapped_data)

    with open(filename, 'w') as f:
        json.dump(all_pokemon_data, f, indent=2)


fetch_and_save_pokemon_data(1, 100)
