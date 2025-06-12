import requests

def get_futurama_characters():
    response = requests.get("https://distansakademin.github.io/api/futurama/characters")

    character_data = response.json()
    print(f"Fetched data successfully")

    return character_data

def get_futurama_episodes():
    response = requests.get("https://distansakademin.github.io/api/futurama/episodes")

    episode_data = response.json()

    return episode_data