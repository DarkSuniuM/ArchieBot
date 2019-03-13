from telegram.ext import Updater, CommandHandler
from config import TOKEN, PROXY


def hello(bot, update):
    update.message.reply_text(
        'Hello {}'.format(update.message.from_user.first_name))


updater = Updater(TOKEN,
                  request_kwargs={'proxy_url': PROXY} if PROXY else None)

updater.dispatcher.add_handler(CommandHandler('hello', hello))

updater.start_polling()
updater.idle()
