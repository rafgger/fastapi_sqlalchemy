# app/utils.py

import requests
from fastapi import HTTPException

def get_coin_id(symbol_or_name):
    """
    Retrieve the CoinGecko coin ID for a given symbol or name.
    """
    url = "https://api.coingecko.com/api/v3/coins/list"
    response = requests.get(url)
    if response.status_code == 200:
        coins = response.json()
        symbol_or_name = symbol_or_name.lower()
        for coin in coins:
            if coin['symbol'].lower() == symbol_or_name or coin['name'].lower() == symbol_or_name:
                return coin['id']
        raise HTTPException(status_code=404, detail="Coin not found")
    else:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch coin list from CoinGecko")