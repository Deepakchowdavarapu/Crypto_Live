import requests
import pandas as pd
import gspread
import time
from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials

def fetch_crypto_data():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        'vs_currency': 'usd',
        'order': 'market_cap_desc',
        'per_page': 50,
        'page': 1,
        'sparkline': False
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None 

def authenticate_gsheet(json_keyfile):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_file(json_keyfile, scopes=scope)
    client = gspread.authorize(creds)
    return client

def update_gsheet(df, sheet_name):
    client = authenticate_gsheet(r'C:\Users\saide\Documents\python\crypto-project-443509-4d7ed8aac23e.json')
    sheet = client.open(sheet_name).sheet1
    sheet.clear()
    sheet.update([df.columns.values.tolist()] + df.values.tolist())

while True:
    try:
        data = fetch_crypto_data()
        if data is None:
            raise Exception("No data returned from API")

        df = pd.DataFrame(data, columns=[
            'name', 'symbol', 'current_price', 'market_cap', 'total_volume', 'price_change_percentage_24h'
        ])
        print("Data fetched and DataFrame created successfully:")
        print(df.head())
        update_gsheet(df, 'Crypto_Live_Data')
    except Exception as e:
        print(f"Error: {e}")

    #5min gap
    time.sleep(300)