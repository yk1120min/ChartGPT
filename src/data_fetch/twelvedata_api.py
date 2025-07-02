import requests
from config import TWELVE_API_KEY

def fetch_data(symbol="USD/JPY",interval="15min", outputsize=500):
    url = "https://api.twelvedata.com/time_series"
    params = {
        "symbol": symbol,
        "interval": interval,
        "outputsize": outputsize,
        "timezone": "Asia/Tokyo",
        "apikey": TWELVE_API_KEY
    }

    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"エラー：{response.status_code}")
        return None
    

