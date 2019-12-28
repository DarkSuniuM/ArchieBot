import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('BOT_TOKEN')
PROXY = os.getenv('BOT_PROXY')
DB_URI = os.getenv('DB_URI')
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
