"""Application's main file."""

import logging
import config

logging.info("=" * 25)
logging.info("Loading modules...")
logging.info("=" * 25)
logging.info("Loading configurations...")
logging.info("=" * 25)
logging.info(f"Path: {config.BASE_DIR}")
logging.info(f"Database: {config.DB_URI}")
logging.info(f"Bot Token: {config.TOKEN}")
logging.info("=" * 25)

from bot import updater
logging.info("Updater Initialized")
logging.info("=" * 25)

logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)

logging.info("Starting polling...")
updater.start_polling()
logging.info("Polling stared")
logging.info("=" * 25)
updater.idle()
logging.info("=" * 25)
logging.info("Stopping the updater...")
updater.stop()
logging.info("=" * 25)