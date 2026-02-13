import os
import requests

from dotenv import load_dotenv
load_dotenv()




API_KEY = os.getenv("ODDS_API_KEY")
SPORT = "soccer_epl"
REGIONS = "eu"
MARKETS = "h2h"

def fetch_odds():
    url = f"https://api.the-odds-api.com/v4/sports/{SPORT}/odds"
    params = {"apiKey": API_KEY, "regions": REGIONS, "markets": MARKETS}
    response = requests.get(url, params=params)

    try:
        data = response.json()
        if isinstance(data, dict) and "message" in data:
            print("❌ API Error:", data["message"])
            return []
        return data
    except Exception as e:
        print("❌ JSON error:", e)
        return []

