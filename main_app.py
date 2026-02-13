import os
import requests
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
import streamlit as st

load_dotenv()
API_KEY = os.getenv("ODDS_API_KEY")

SPORT_KEYS = [
    "soccer_international_friendly",
]

REGIONS = "eu"
MARKETS = "totals"  # över/under
BANKROLL = 1000
UNIT_SIZE = 0.01  # 1 % av bankroll


def fetch_matches():
    all_matches = []
    for sport in SPORT_KEYS:
        url = f"https://api.the-odds-api.com/v4/sports/{sport}/odds"
        params = {
            "apiKey": API_KEY,
            "regions": REGIONS,
            "markets": MARKETS,
            "oddsFormat": "decimal",
            "dateFormat": "iso"
        }
        res = requests.get(url, params=params)
        if res.status_code != 200:
            st.warning(f"API-fel för {sport}: {res.status_code}")
            continue
        all_matches.extend(res.json())
    return all_matches


def calculate_ev(our_prob, odds):
    return our_prob * (odds - 1) - (1 - our_prob)


def suggest_bet(ev, max_units=5):
    if ev <= 0:
        return 0
    units = min(max_units, max(1, int(ev / 0.04)))
    return units


def dummy_total_goal_probs():
    # Dummy: 55% chans för över 2.5 mål, 45% under – byt ut med statistik/modell!
    return {"over_2.5": 0.55, "under_2.5": 0.45}


def main():
    matches = fetch_matches()
    rows = []

    for event in matches:
        home = event["home_team"]
        away = event["away_team"]
        commence = datetime.fromisoformat(event["commence_time"].replace("Z", "+00:00"))

        best_odds = {}
        for bookmaker in event.get("bookmakers", []):
            for market in bookmaker.get("markets", []):
                if market.get("key") != "totals":
                    continue
                for outcome in market.get("outcomes", []):
                    # Filtrera endast 2.5-målslinan
                    if float(outcome.get("point", 0)) != 2.5:
                        continue
                    name = outcome["name"].lower()  # 'over' eller 'under'
                    price = outcome.get("price", 0)
                    if price > best_odds.get(name, 0):
                        best_odds[name] = price

        # Kontrollera att båda odds finns
        if "over" not in best_odds or "under" not in best_odds:
            continue

        # Dummy-sannolikheter — byt ut mot egen modell om du vill
        prob_over = 0.55
        prob_under = 0.45

        ev_over = calculate_ev(prob_over, best_odds["over"])
        ev_under = calculate_ev(prob_under, best_odds["under"])

        for outcome, ev, prob in [
            ("Över 2.5 mål", ev_over, prob_over),
            ("Under 2.5 mål", ev_under, prob_under)
        ]:
            if ev <= 0:
                continue

            units = suggest_bet(ev)
            stake = units * UNIT_SIZE * BANKROLL

            rows.append({
                "Match": f"{home} - {away}",
                "Outcome": outcome,
                "Odds": round(best_odds.get(outcome.split()[0].lower(), 0), 2),
                "Probability": round(prob, 2),
                "EV": round(ev, 3),
                "Units": units,
                "Stake (SEK)": round(stake, 2),
                "Starttid": commence.strftime("%Y-%m-%d %H:%M UTC"),
            })

    if not rows:
        st.subheader("Dagens Bettingval - Över/Under 2.5 mål")
        st.warning("Inga spel med positiv EV hittades idag för över/under 2.5 mål.")
        return

    df = pd.DataFrame(rows)
    df = df.sort_values("EV", ascending=False).drop_duplicates(subset=["Match", "Outcome"])

    st.subheader("Dagens Bettingval - Över/Under 2.5 mål")
    st.dataframe(df.reset_index(drop=True), use_container_width=True)


if __name__ == "__main__":
    main()
