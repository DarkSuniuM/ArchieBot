"""Bot module main file."""
from telegram import ChatPermissions
from telegram.ext import CallbackQueryHandler, Filters, MessageHandler, Updater

from config import PROXY, TOKEN


RESTRICTED_PERMISSIONS = ChatPermissions(can_send_messages=False)
UNRESTRICTED_PERMISSIONS = ChatPermissions(can_send_messages=True)

updater = Updater(TOKEN,
                  request_kwargs={'proxy_url': PROXY} if PROXY else None,
                  use_context=True)


from .handlers import check_user, kick_bots, check_answer, error_handler

updater.dispatcher.add_handler(
    MessageHandler(Filters.status_update.new_chat_members, kick_bots)
)
updater.dispatcher.add_handler(
    MessageHandler(Filters.all, check_user)
)


updater.dispatcher.add_handler(
    CallbackQueryHandler(check_answer)
)
updater.dispatcher.add_error_handler(error_handler)

