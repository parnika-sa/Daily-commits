import json
import os
import requests


def fetch_hacker_news_top():
    top_stories_url = "https://hacker-news.firebaseio.com/v0/topstories.json"
    item_url = "https://hacker-news.firebaseio.com/v0/item/{item_id}.json"

    try:
        response = requests.get(top_stories_url, timeout=10)
        response.raise_for_status()
        story_ids = response.json()[:10]

        stories = []
        for story_id in story_ids:
            item_response = requests.get(item_url.format(item_id=story_id), timeout=10)
            item_response.raise_for_status()
            story = item_response.json() or {}
            if story.get("type") != "story":
                continue

            stories.append(
                {
                    "title": story.get("title", "Untitled"),
                    "url": story.get("url", f"https://news.ycombinator.com/item?id={story_id}"),
                    "score": story.get("score", 0),
                    "comments": story.get("descendants", 0),
                }
            )

            if len(stories) >= 5:
                break

        os.makedirs("data", exist_ok=True)
        output_path = os.path.join("data", "hacker_news.json")
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(stories, f, indent=4, ensure_ascii=False)

        print(f"Successfully fetched {len(stories)} Hacker News stories.")

    except Exception as e:
        print(f"Error fetching Hacker News data: {e}")


if __name__ == "__main__":
    fetch_hacker_news_top()
