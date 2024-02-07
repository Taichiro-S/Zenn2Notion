import zenn_api
import notion_api
import config

REMEMBER_USER_TOKEN = config.REMEMBER_USER_TOKEN
NOTION_DATABASE_ID_FOR_BOOKS = config.NOTION_DATABASE_ID_FOR_BOOKS
NOTION_SECRET = config.NOTION_SECRET

cookie = f"remember_user_token={REMEMBER_USER_TOKEN}"

old_books_urls = notion_api.fetch_urls(NOTION_DATABASE_ID_FOR_BOOKS, NOTION_SECRET)
print(f"Found {len(old_books_urls)} books in Notion database.")

new_books = zenn_api.fetch_reading_books(cookie, old_books_urls)
print(f"Found {len(new_books)} new books in Zenn Reading books.")

for i, book in enumerate(new_books):
    print(f"Inserting book {i+1}...")
    notion_api.insert_book(NOTION_DATABASE_ID_FOR_BOOKS, book, NOTION_SECRET)
