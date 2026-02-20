import json
import os
from datetime import datetime
import pandas as pd

def generate_dashboard():
    github_data_path = os.path.join('data', 'github_trending.json')
    crypto_data_path = os.path.join('data', 'crypto.json')
    
    # Load Data
    github_repos = []
    if os.path.exists(github_data_path):
        with open(github_data_path, 'r', encoding='utf-8') as f:
            github_repos = json.load(f)
            
    crypto_data = {}
    if os.path.exists(crypto_data_path):
        with open(crypto_data_path, 'r', encoding='utf-8') as f:
            crypto_data = json.load(f)
            
    # Prepare Content
    now_utc = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')
    
    # Header
    content = f"# Daily Automation Intelligence Engine\n\n"
    content += f"**Last Updated:** `{now_utc}`\n\n"
    
    # Automated Summary
    summary = "This dashboard is automatically updated every day. "
    if github_repos:
        top_repo = github_repos[0]['name']
        summary += f"The top trending repository today is **{top_repo}**. "
    if crypto_data:
        btc_price = crypto_data.get('bitcoin', {}).get('price_usd', 'N/A')
        summary += f"Bitcoin is currently trading at **${btc_price:,} USD**."
    
    content += f"## 🤖 Automated Summary\n{summary}\n\n"
    
    # Crypto Section
    content += "## 💰 Crypto Snapshot\n"
    if crypto_data:
        content += "| Asset | Price (USD) |\n"
        content += "| :--- | :--- |\n"
        for asset, stats in crypto_data.items():
            price = f"${stats['price_usd']:,}"
            content += f"| {asset.capitalize()} | {price} |\n"
    else:
        content += "_Crypto data unavailable._\n"
    content += "\n"
    
    # GitHub Trending Section
    content += "## 🚀 Top 5 Trending Repositories\n"
    if github_repos:
        content += "| Repository | Language | Stars Today | Description |\n"
        content += "| :--- | :--- | :--- | :--- |\n"
        for repo in github_repos[:5]:
            name = repo['name']
            # GitHub trending links are usually relative or just name/repo
            link = f"https://github.com/{name}"
            desc = repo['description'][:100] + "..." if len(repo['description']) > 100 else repo['description']
            content += f"| [{name}]({link}) | {repo['language']} | {repo['stars_today']} | {desc} |\n"
    else:
        content += "_GitHub trending data unavailable._\n"
        
    # Write to README.md
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(content)
        
    print("README.md dashboard successfully generated.")

if __name__ == "__main__":
    generate_dashboard()
