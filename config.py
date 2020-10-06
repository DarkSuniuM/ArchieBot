import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('BOT_TOKEN')
PROXY = os.getenv('BOT_PROXY')
RECOVERY_CHAT_ID = os.getenv('BOT_RECOVERY_CHAT_ID')
DB_URI = os.getenv('DB_URI')
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
