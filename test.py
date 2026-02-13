import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("ODDS_API_KEY")

def get_sports():
    url = "https://api.the-odds-api.com/v4/sports"
    params = {"apiKey": API_KEY}
    response = requests.get(url, params=params)
    if response.status_code != 200:
        print("Fel vid API-anrop:", response.status_code, response.text)
        return []
    sports = response.json()
    for sport in sports:
        print(f"{sport['key']}: {sport['title']}")
    return sports

if __name__ == "__main__":
    get_sports()
