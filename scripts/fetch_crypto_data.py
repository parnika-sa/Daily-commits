import requests
import json
import os

def fetch_crypto_prices():
    # CoinGecko Simple Price API
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": "bitcoin,ethereum,solana,binancecoin",
        "vs_currencies": "usd",
        "include_24hr_change": "true"
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        crypto_snapshot = {
            "bitcoin": {
                "price_usd": data["bitcoin"]["usd"],
                "change_24h": data["bitcoin"].get("usd_24h_change", 0.0)
            },
            "ethereum": {
                "price_usd": data["ethereum"]["usd"],
                "change_24h": data["ethereum"].get("usd_24h_change", 0.0)
            },
            "solana": {
                "price_usd": data["solana"]["usd"],
                "change_24h": data["solana"].get("usd_24h_change", 0.0)
            },
            "bnb": {
                "price_usd": data["binancecoin"]["usd"],
                "change_24h": data["binancecoin"].get("usd_24h_change", 0.0)
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
