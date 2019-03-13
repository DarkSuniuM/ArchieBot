import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('BOT_TOKEN')
PROXY = os.getenv('BOT_PROXY') or None
