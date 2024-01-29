import zenn_api
import notion_api
import config

REMEMBER_USER_TOKEN = config.REMEMBER_USER_TOKEN
NOTION_DATABASE_ID = config.NOTION_DATABASE_ID
NOTION_SECRET = config.NOTION_SECRET

cookie = f"remember_user_token={REMEMBER_USER_TOKEN}"

old_likes_urls = notion_api.fetch_article_urls(NOTION_DATABASE_ID, NOTION_SECRET)
print(f"Found {len(old_likes_urls)} articles in Notion database.")

new_likes = zenn_api.fetch_likes(cookie, old_likes_urls)
print(f"Found {len(new_likes)} new articles in Zenn likes.")

for i, article in enumerate(new_likes):
    print(f"Inserting article {i+1}...")
    notion_api.insert_article(NOTION_DATABASE_ID, article, NOTION_SECRET, article.get("emoji"))
