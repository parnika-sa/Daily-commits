import requests
import json
import os

def fetch_crypto_prices():
    # CoinGecko Simple Price API
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": "bitcoin,ethereum",
        "vs_currencies": "usd"
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        crypto_snapshot = {
            "bitcoin": {
                "price_usd": data["bitcoin"]["usd"]
            },
            "ethereum": {
                "price_usd": data["ethereum"]["usd"]
            }
        }
        
        # Ensure data directory exists
        os.makedirs('data', exist_ok=True)
        
        output_path = os.path.join('data', 'crypto.json')
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(crypto_snapshot, f, indent=4)
            
        print("Successfully fetched crypto prices.")
        
    except Exception as e:
        print(f"Error fetching crypto data: {e}")

if __name__ == "__main__":
    fetch_crypto_prices()
