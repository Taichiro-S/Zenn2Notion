import time
import requests

ARTICLE_URL = 'https://zenn.dev/api/articles/'
BOOK_URL = 'https://zenn.dev/api/books/'
LIKES_URL = 'https://zenn.dev/api/me/library/likes'
READING_BOOKS_URL = 'https://zenn.dev/api/me/library/reading_book_histories'
TIMEOUT = 5
# 1秒間隔でAPIリクエストを送る
INTERVAL = 1

def fetch_article_topics(slug):
    url = f"{ARTICLE_URL}{slug}"
    response = requests.get(url, timeout=TIMEOUT)

    if response.status_code != 200:
        print(f"Error: Unable to fetch topics for article {slug}.")
        print(response.text)
        return None
    print(f"Successfully fetched topics for article {slug}.")
    return response.json().get("article")

def fetch_book_details(slug):
    url = f"{BOOK_URL}{slug}"
    response = requests.get(url, timeout=TIMEOUT)
    if response.status_code != 200:
        print(f"Error: Unable to fetch details for book {slug}.")
        print(response.text)
        return None
    print(f"Successfully fetched details for book {slug}.")
    return response.json().get("book")

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
            print(f"Error: Unable to fetch data. Message: {response.text}")
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
            details = fetch_article_topics(slug)
            if details:
                article["topics"] = [topic["name"] for topic in details.get("topics", [])]
            time.sleep(INTERVAL)
        all_articles.extend(articles)
        page += 1
        time.sleep(INTERVAL)
    all_articles.reverse()
    filtered_articles = [article for article in all_articles if f"https://zenn.dev{article.get('path')}" not in urls]
    return filtered_articles

def fetch_reading_books(cookie, urls):
    headers = {
        "Cookie": cookie,
    }

    all_books = []
    page = 1
    stop_fetching = False
    
    while not stop_fetching:
        print(f"Fetching page {page}...")
        params = {"page": page}
        response = requests.get(READING_BOOKS_URL, headers=headers, params=params, timeout=TIMEOUT) 
        if response.status_code != 200:
            print(f"Error: Unable to fetch data. Message: {response.text}")
            break
        data = response.json()
        books = data.get("books", [])
        next_page = data.get("next_page")
        if not books or next_page is None:
            print("No more pages to fetch.")
            break
        for i, book in enumerate(books):
            slug = book.get("book").get("slug")
            username = book.get("book").get("user").get("username")
            book_url = f"https://zenn.dev/{username}/books/{slug}"
            if book_url in urls:
                print(f"Book {i+1} is already in Notion database. Stop fetching.")
                stop_fetching = True
                break
            print(f"Fetching book {i+1}...")
            details = fetch_book_details(slug)
            if details:
                book["topics"] = [topic["name"] for topic in details.get("topics", [])]
                book['can_read_all_chapters'] = details['can_read_all_chapters']
                book['chapter_count'] = len(details['chapters'])
            time.sleep(INTERVAL)
        all_books.extend(books)
        page += 1
        time.sleep(INTERVAL)
    all_books.reverse()
    filtered_books = [book for book in all_books if f"https://zenn.dev/{book.get('book').get('user').get('username')}/books/{book.get('book').get('slug')}" not in urls]
    return filtered_books