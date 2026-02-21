import json
import os
from datetime import datetime, UTC

def generate_dashboard():
    github_data_path = os.path.join('data', 'github_trending.json')
    crypto_data_path = os.path.join('data', 'crypto.json')
    hacker_news_data_path = os.path.join('data', 'hacker_news.json')
    run_health_data_path = os.path.join('data', 'run_health.json')
    
    # Load Data
    github_repos = []
    if os.path.exists(github_data_path):
        with open(github_data_path, 'r', encoding='utf-8') as f:
            github_repos = json.load(f)
            
    crypto_data = {}
    if os.path.exists(crypto_data_path):
        with open(crypto_data_path, 'r', encoding='utf-8') as f:
            crypto_data = json.load(f)

    hacker_news = []
    if os.path.exists(hacker_news_data_path):
        with open(hacker_news_data_path, 'r', encoding='utf-8') as f:
            hacker_news = json.load(f)

    run_health = {}
    if os.path.exists(run_health_data_path):
        with open(run_health_data_path, 'r', encoding='utf-8') as f:
            run_health = json.load(f)
            
    # Prepare Content
    now_utc = datetime.now(UTC).strftime('%Y-%m-%d %H:%M:%S UTC')
    
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
    if hacker_news:
        summary += f" Top Hacker News story: **{hacker_news[0]['title']}**."
    
    content += f"## 🤖 Automated Summary\n{summary}\n\n"

    content += "## 🩺 Run Health\n"
    if run_health:
        content += "| Metric | Value |\n"
        content += "| :--- | :--- |\n"
        content += f"| Last Run (UTC) | {run_health.get('last_run_utc', 'N/A')} |\n"
        content += f"| Last Run (IST) | {run_health.get('last_run_ist', 'N/A')} |\n"
        content += f"| Daily Target | {run_health.get('target_commits_per_day', 'N/A')} |\n"
        content += f"| Commits Today (IST) | {run_health.get('commits_today', 'N/A')} |\n"
        content += f"| Remaining Today | {run_health.get('remaining_today', 'N/A')} |\n"
        content += f"| Status | {run_health.get('status', 'N/A')} |\n"
    else:
        content += "_Run health data unavailable._\n"
    content += "\n"
    
    # Crypto Section
    content += "## 💰 Crypto Snapshot\n"
    if crypto_data:
        content += "| Asset | Price (USD) | 24h Change |\n"
        content += "| :--- | :--- | :--- |\n"
        for asset, stats in crypto_data.items():
            price = f"${stats['price_usd']:,}"
            change_24h = stats.get('change_24h', 0.0)
            change_str = f"{change_24h:+.2f}%"
            content += f"| {asset.capitalize()} | {price} | {change_str} |\n"
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

    content += "\n## 📰 Top Hacker News Stories\n"
    if hacker_news:
        content += "| Story | Score | Comments |\n"
        content += "| :--- | :--- | :--- |\n"
        for story in hacker_news[:5]:
            title = story.get('title', 'Untitled')
            url = story.get('url', '#')
            score = story.get('score', 0)
            comments = story.get('comments', 0)
            content += f"| [{title}]({url}) | {score} | {comments} |\n"
    else:
        content += "_Hacker News data unavailable._\n"
        
    # Write to README.md
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(content)
        
    print("README.md dashboard successfully generated.")

if __name__ == "__main__":
    generate_dashboard()
