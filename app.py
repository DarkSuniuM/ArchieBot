from telegram.ext import Updater, Filters, MessageHandler
from config import TOKEN, PROXY


def kickBots(bot, update):
    for new_user in update.message.new_chat_members:
        if new_user.is_bot:
            bot.kickChatMember(update.message.chat.id, new_user.id, timeout=5)


updater = Updater(TOKEN,
                  request_kwargs={'proxy_url': PROXY} if PROXY else None)

updater.dispatcher.add_handler(
    MessageHandler(Filters.status_update.new_chat_members, kickBots))

updater.start_polling()
updater.idle()
