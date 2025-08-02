import requests, pandas as pd
def get_10k_facts(ticker):
    url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{ticker}.json"
    headers = {"User-Agent": "your.email@example.com"}
    return requests.get(url, headers=headers).json()