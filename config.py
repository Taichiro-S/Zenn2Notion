import os
from dotenv import load_dotenv

load_dotenv()

NOTION_API_KEY = os.getenv('NOTION_API_KEY')
ZENN_SESSION = os.getenv('ZENN_SESSION')
REMEMBER_TOKEN = os.getenv('REMEMBER_TOKEN')
NOTION_DATABASE_ID = os.getenv('NOTION_DATABASE_ID')
