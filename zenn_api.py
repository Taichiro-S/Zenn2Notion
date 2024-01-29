import time
import requests

ARTICLE_URL = 'https://zenn.dev/api/articles/'
LIKES_URL = 'https://zenn.dev/api/me/library/likes'
TIMEOUT = 10
# 1秒間隔でAPIリクエストを送る
INTERVAL = 1

def fetch_article_details(slug):
    url = f"{ARTICLE_URL}{slug}"
    response = requests.get(url, timeout=TIMEOUT)

    if response.status_code != 200:
        print(f"Error: Unable to fetch details for article {slug}.")
        print(response.text)
        return None
    print(f"Successfully fetched details for article {slug}.")
    return response.json().get("article")

def fetch_likes(cookie, urls):
    headers = {
        "Cookie": cookie,
    }

    all_articles = []
    page = 1
    stop_fetching = False
    
    while not stop_fetching:
        print(f"Fetching page {page}...")
        params = {"page": page}
        response = requests.get(LIKES_URL, headers=headers, params=params, timeout=TIMEOUT) 
        if response.status_code != 200:
            print(f"Error: Unable to fetch data. Message: {response.message}")
            break
        data = response.json()
        articles = data.get("items", [])
        next_page = data.get("next_page")
        if not articles or next_page is None:
            print("No more pages to fetch.")
            break
        for i, article in enumerate(articles):
            article_url = f"https://zenn.dev{article.get('path')}"
            if article_url in urls:
                print(f"Article {i+1} is already in Notion database. Stop fetching.")
                stop_fetching = True
                break
            print(f"Fetching article {i+1}...")
            slug = article.get("slug")
            details = fetch_article_details(slug)
            if details:
                article["body_html"] = details.get("body_html")
                article["topics"] = [topic["name"] for topic in details.get("topics", [])]
            time.sleep(INTERVAL)
        all_articles.extend(articles)
        page += 1
        time.sleep(INTERVAL)
    all_articles.reverse()
    filtered_articles = [article for article in all_articles if f"https://zenn.dev{article.get('path')}" not in urls]
    return filtered_articles
