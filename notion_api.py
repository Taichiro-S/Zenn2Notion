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


def fetch_article_urls(database_id, NOTION_SECRET):
    url = f"{DATABASE_URL}{database_id}/query"
    headers = {
        "Authorization": f"Bearer {NOTION_SECRET}",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json"
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
            raise requests.exceptions.HTTPError(f"Failed to query database: {response.text}")

        data = response.json()
        links.extend([page['properties']['link']['url'] for page in data['results'] if 'link' in page['properties']])

        has_more = data.get("has_more", False)
        start_cursor = data.get("next_cursor", None)
    return links

def insert_article(database_id, article, NOTION_SECRET, emoji):
    headers = {
        "Accept": "application/json",
        'Authorization': f'Bearer {NOTION_SECRET}',
        'Notion-Version': NOTION_VERSION,
        'Content-Type': 'application/json',
    }
    page_properties = {
        'parent': {
            "type": "database_id",
            "database_id": database_id,
        },
        'icon': {'type': 'emoji', 'emoji': emoji},
        'properties': {
            'title': {
                'title': [
                    {
                        'text': {
                            'content': article.get("title"),
                        },
                    },
                ],
            },
            'author': {
                'rich_text': [
                    {
                        'type': 'text',
                        'text': {
                            'content': article.get("user", {}).get("name"),
                            'link': {'url': f"https://zenn.dev/{article.get('user', {}).get('username')}"}
                        }
                    }
                ]
            },
            'topic': {
                'multi_select': [{'name': topic} for topic in article.get("topics", [])]
            },
            'published_at': {
                'date': {
                    'start': article.get("published_at"),
                },
            },
            'link': {
                'url': f"https://zenn.dev{article.get('path')}",
            },
        },
    }

    response = requests.post(PAGE_URL, headers=headers, data=json.dumps(page_properties), timeout=TIMEOUT)
    if response.status_code != 200:
        if "emoji" in response.text:
            print("Emoji not supported, retrying with default emoji...")
            return insert_article(database_id, article, NOTION_SECRET, DEFAULT_EMOJI)
        raise requests.exceptions.HTTPError(f'Failed to create page: {response.text}')
    print(f"Article '{article.get('title')}' inserted successfully.")
