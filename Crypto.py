import time
import pandas as pd
import requests
import xlwings as xw
import os

def fetch_crypto_data():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        'vs_currency': 'usd',
        'order': 'market_cap_desc',
        'per_page': 50,
        'page': 1,
        'sparkline': False
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Failed to fetch data")


def create_or_update_excel(dataframe, file_name="Crypto_Live_Data.xlsx"):
    if not os.path.exists(file_name):
        wb = xw.Book() 
        wb.save(file_name) 
        wb.close()
    
    wb = xw.Book(file_name)
    sheet = wb.sheets[0]
    sheet.range("A1").value = dataframe 


while True:
    data = fetch_crypto_data()
    df = pd.DataFrame(data, columns=[
        'name', 'symbol', 'current_price', 'market_cap', 'total_volume', 'price_change_percentage_24h'
    ])
    
    create_or_update_excel(df)    
    time.sleep(300)
