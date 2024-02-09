import requests
import json
import html2text

DEFAULT_EMOJI = "😅"
DATABASE_URL = "https://api.notion.com/v1/databases/"
PAGE_URL = "https://api.notion.com/v1/pages/"
NOTION_VERSION = "2021-08-16"
TIMEOUT = 10


def html_to_markdown(html):
    converter = html2text.HTML2Text()
    converter.ignore_links = False
    return converter.handle(html)


def fetch_urls(database_id, notion_secret):
    url = f"{DATABASE_URL}{database_id}/query"
    headers = {
        "Authorization": f"Bearer {notion_secret}",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json",
    }

    links = []
    has_more = True
    start_cursor = None

    while has_more:
        payload = {}
        if start_cursor:
            payload["start_cursor"] = start_cursor

        response = requests.post(url, headers=headers, json=payload, timeout=TIMEOUT)
        if response.status_code != 200:
            raise requests.exceptions.HTTPError(
                f"Failed to query database: {response.text}"
            )

        data = response.json()
        links.extend(
            [
                page["properties"]["リンク"]["url"]
                for page in data["results"]
                if "リンク" in page["properties"]
            ]
        )

        has_more = data.get("has_more", False)
        start_cursor = data.get("next_cursor", None)
    return links


def insert_article(database_id, article, notion_secret, emoji):
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {notion_secret}",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json",
    }
    page_properties = {
        "parent": {
            "type": "database_id",
            "database_id": database_id,
        },
        "icon": {"type": "emoji", "emoji": emoji},
        "properties": {
            "タイトル": {
                "title": [
                    {
                        "text": {
                            "content": article.get("title"),
                        },
                    },
                ],
            },
            "著者": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {
                            "content": article.get("user", {}).get("name"),
                            "link": {
                                "url": f"https://zenn.dev/{article.get('user', {}).get('username')}"
                            },
                        },
                    }
                ]
            },
            # 記事につけられたトピック
            "トピック": {
                "multi_select": [{"name": topic} for topic in article.get("topics", [])]
            },
            "公開日": {
                "date": {
                    "start": article.get("published_at"),
                },
            },
            "リンク": {
                "url": f"https://zenn.dev{article.get('path')}",
            },
        },
    }

    response = requests.post(
        PAGE_URL, headers=headers, data=json.dumps(page_properties), timeout=TIMEOUT
    )
    if response.status_code != 200:
        if "emoji" in response.text:
            print("Emoji not supported, retrying with default emoji...")
            return insert_article(database_id, article, notion_secret, DEFAULT_EMOJI)
        raise requests.exceptions.HTTPError(f"Failed to create page: {response.text}")
    print(f"Article '{article.get('title')}' inserted successfully.")


def insert_book(database_id, book, notion_secret):
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {notion_secret}",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json",
    }
    page_properties = {
        "parent": {
            "type": "database_id",
            "database_id": database_id,
        },
        "icon": {"type": "emoji", "emoji": "📚"},
        "properties": {
            "タイトル": {
                "title": [
                    {
                        "text": {
                            "content": book.get("book").get("title"),
                        },
                    },
                ],
            },
            "著者": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {
                            "content": book.get("book").get("user", {}).get("name"),
                            "link": {
                                "url": f"https://zenn.dev/{book.get('book').get('user', {}).get('username')}"
                            },
                        },
                    }
                ]
            },
            "トピック": {
                "multi_select": [{"name": topic} for topic in book.get("topics", [])]
            },
            "公開日": {
                "date": {
                    "start": book.get("book").get("published_at"),
                },
            },
            "リンク": {
                "url": f"https://zenn.dev{book.get('book').get('path')}",
            },
            "読み始めた日": {
                "date": {
                    "start": book.get("read_at"),
                },
            },
            "値段": {
                "number": book.get("book").get("price"),
            },
            "全てのチャプターが公開されているか": {
                "checkbox": book.get("can_read_all_chapters", False),
            },
            "チャプター数": {
                "number": book.get("chapter_count"),
            },
        },
    }

    response = requests.post(
        PAGE_URL, headers=headers, data=json.dumps(page_properties), timeout=TIMEOUT
    )
    if response.status_code != 200:
        raise requests.exceptions.HTTPError(f"Failed to create page: {response.text}")
    print(f"Book '{book.get('book').get('title')}' inserted successfully.")
