import requests

def get_pokemon_data(pname):
   
    url = f"https://pokeapi.co/api/v2/pokemon/{pname.lower()}"
    response = requests.get(url)
    
    if response.status_code != 200:
        return "red" if response.status_code == 404 else "black", None

    data = response.json()
    
    
    species_url = data['species']['url']
    species_resp = requests.get(species_url).json()
    
    
    flavor_texts = [entry['flavor_text'] for entry in species_resp['flavor_text_entries'] if entry['language']['name'] == 'en']
    
   
    pokemon_info = {
        "id": data.get("id"),
        "name": data.get("name"),
        "height": data.get("height"),
        "weight": data.get("weight") / 10,
        "img": data.get("sprites", {}).get("other", {}).get("official-artwork", {}).get("front_default"),
        "types": [t["type"]["name"] for t in data.get("types", [])],
        "abilities": [a["ability"]["name"] for a in data.get("abilities", [])],
        "stats": {s["stat"]["name"]: s["base_stat"] for s in data.get("stats", [])},
        "moves": [m["move"]["name"] for m in data.get("moves", [])],
        "flavor_text": flavor_texts[0] if flavor_texts else "No description available.",
        "is_legendary": species_resp.get("is_legendary"),
        "capture_rate": species_resp.get("capture_rate")
    }
    
    return "green", pokemon_info