"""Application's main file."""

import logging

from bot import updater


logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)

updater.start_polling()
updater.idle()
