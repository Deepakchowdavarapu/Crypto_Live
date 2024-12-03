import requests
import pandas as pd
import gspread
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
        response.raise_for_status()  # Will raise an exception for 4xx/5xx status codes
        return response.json()  # Return JSON data if the response is okay
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None  # Return None in case of failure

def authenticate_gsheet(json_keyfile):
    credentials = Credentials.from_service_account_file(
        json_keyfile, 
        scopes=["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    )
    
    # Ensure the credentials are valid
    if credentials.expired and credentials.refresh_token:
        credentials.refresh(Request())
    
    client = gspread.authorize(credentials)
    return client

def update_gsheet(dataframe, sheet_name, worksheet_index=0):
    try:
        client = authenticate_gsheet(r'C:\Users\saide\Documents\python\crypto-project-443509-4d7ed8aac23e.json')
        sheet = client.open(sheet_name)
        worksheet = sheet.get_worksheet(worksheet_index)        
        data = [dataframe.columns.values.tolist()] + dataframe.values.tolist()        
        cell_list = worksheet.range(1, 1, len(data), len(data[0]))
        for i, cell in enumerate(cell_list):
            row, col = divmod(i, len(data[0]))
            cell.value = data[row][col]
        worksheet.update_cells(cell_list)
        print(f"Successfully updated the sheet: {sheet_name}")
    except Exception as e:
        print(f"Error updating Google Sheet: {e}")


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
