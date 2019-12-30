"""Bot module main file."""
from telegram import ChatPermissions, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import CallbackQueryHandler, Filters, MessageHandler, Updater, InlineQueryHandler


from config import PROXY, TOKEN


RESTRICTED_PERMISSIONS = ChatPermissions(can_send_messages=False)
UNRESTRICTED_PERMISSIONS = ChatPermissions(can_send_messages=True)

updater = Updater(TOKEN,
                  request_kwargs={'proxy_url': PROXY} if PROXY else None,
                  use_context=True)
dp = updater.dispatcher
job_queue = updater.job_queue


from .handlers import check_user, kick_bots, check_answer, error_handler, inlinequery

dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, kick_bots))
dp.add_handler(MessageHandler(Filters.all, check_user))

dp.add_handler(InlineQueryHandler(inlinequery))

dp.add_handler(CallbackQueryHandler(check_answer))

dp.add_error_handler(error_handler)

from .jobs import delete_pending_activation_messages

job_queue.run_repeating(delete_pending_activation_messages, 10)
