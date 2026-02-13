# Football Odds Data Pipeline & Analysis

## Overview
This project fetches football match and odds data from an external API, processes the data, and performs probability analysis using a Poisson-based model. The purpose of the project is to demonstrate data pipeline design, API integration, structured code organization, and analytical modeling in Python.

## Features
- Fetches match/odds data from API
- Processes and structures raw JSON data
- Applies Poisson distribution model for goal probability estimation
- Modular code structure (separation of concerns)
- Designed for further extension into database storage or visualization

## Project Structure

main_app.py – Entry point of the application  
odds_fetcher.py – Handles API requests and data retrieval  
poisson_model.py – Implements probability calculations  
test.py – Basic test logic  

## Technologies Used
- Python 3
- requests
- JSON handling
- Poisson distribution (statistical modeling)

## How to Run

1. Clone the repository: git clone https://github.com/johankurt7/Football_odds_analysis.git
2. Install dependencies
3. Add your API key in a `.env` file:
4. Run the application:


## What I Learned
- Structuring Python projects
- Handling external APIs and JSON data
- Implementing probability models for real-world data
- Writing readable and maintainable code

## Future Improvements
- Store data in SQL
- Add logging and error handling
- Add data visualization