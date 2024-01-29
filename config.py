import os
from dotenv import load_dotenv

load_dotenv()

NOTION_SECRET = os.getenv('NOTION_SECRET')
NOTION_DATABASE_ID = os.getenv('NOTION_DATABASE_ID')
REMEMBER_USER_TOKEN = os.getenv('REMEMBER_USER_TOKEN')

