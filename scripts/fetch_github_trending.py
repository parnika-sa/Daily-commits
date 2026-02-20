import requests
from bs4 import BeautifulSoup
import json
import os

def fetch_trending_repos():
    url = "https://github.com/trending"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        repos = []
        
        for article in soup.select('article.Box-row'):
            repo_name_tag = article.select_one('h2 a')
            repo_name = repo_name_tag.text.strip().replace('\n', '').replace(' ', '') if repo_name_tag else "Unknown"
            
            description_tag = article.select_one('p.col-9')
            description = description_tag.text.strip() if description_tag else "No description"
            
            language_tag = article.select_one('[itemprop="programmingLanguage"]')
            language = language_tag.text.strip() if language_tag else "Unknown"
            
            stars_today_tag = article.select_one('span.d-inline-block.float-sm-right')
            stars_today = stars_today_tag.text.strip() if stars_today_tag else "0 stars today"
            
            repos.append({
                "name": repo_name,
                "description": description,
                "language": language,
                "stars_today": stars_today
            })
            
        # Ensure data directory exists
        os.makedirs('data', exist_ok=True)
        
        output_path = os.path.join('data', 'github_trending.json')
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(repos, f, indent=4, ensure_ascii=False)
            
        print(f"Successfully fetched {len(repos)} repositories.")
        
    except Exception as e:
        print(f"Error fetching trending repos: {e}")

if __name__ == "__main__":
    fetch_trending_repos()
