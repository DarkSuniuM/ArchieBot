"""Application's main file."""

import logging
import config

print("=" * 25)
print("Loading modules...")
print("=" * 25)
print("Loading configurations...")
print("=" * 25)
print(f"Path: {config.BASE_DIR}")
print(f"Database: {config.DB_URI}")
print(f"Bot Token: {config.TOKEN}")
print("=" * 25)

from bot import updater
print("Updater Initialized")
print("=" * 25)

logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)

print("Starting polling...")
updater.start_polling()
print("Polling stared")
print("=" * 25)
updater.idle()
print("=" * 25)
print("Stopping the updater...")
updater.stop()
print("=" * 25)