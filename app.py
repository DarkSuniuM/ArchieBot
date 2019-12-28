from random import randint, sample, shuffle

import logging
import datetime as dt
import traceback

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, ChatPermissions
from telegram.ext import CallbackQueryHandler, Filters, MessageHandler, Updater

from config import PROXY, TOKEN
from models import User


restricted_permissions = ChatPermissions(can_send_messages=False)
unrestricted_permissions = ChatPermissions(can_send_messages=True)


def captchaGenerator(user_id, group_id):
    first_operator = 2
    second_operator = randint(1, 10)
    correct_answer = first_operator * second_operator
    equation = f"{first_operator} * {second_operator}"
    all_answers = answerGenerator(correct_answer, 4)
    inline_buttons = []
    for answer in all_answers:
        data = f"{user_id},{group_id},{int(answer == correct_answer) or -answer}"
        button = InlineKeyboardButton(answer, callback_data=data)
        inline_buttons.append(button)
    return (equation, correct_answer, inline_buttons)


def answerGenerator(correct_answer, length):
    first_list = list(range(0, correct_answer))
    second_list = list(range(correct_answer + 1, length))
    random_generated_list = sample(first_list + second_list, length - 1)
    random_generated_list.append(correct_answer)
    shuffle(random_generated_list)
    return random_generated_list


def kickBots(update, context):
    for new_user in update.message.new_chat_members:
        if new_user.is_bot and new_user.id != context.bot.id:
            context.bot.kickChatMember(update.message.chat.id, new_user.id, timeout=5)
        if not new_user.is_bot:
            checkUser(update, context)


def checkUser(update, context):
    group_id = update.message.chat.id
    user_id = update.message.from_user.id
    print(user_id)
    message_time = update.message.date.timestamp()


    if user_id == 777000:
        # Telegram uses it's official account with 
        # the id '777000' to forward channel messages
        # to linked group,
        # Therefor We need to check if the message
        # came from this special '777000' id or not!
        return
    if message_time + 5 < dt.datetime.utcnow().timestamp():
        return
    if user_id == context.bot.id:
        return
    user = User.get_or_create(user_tid=user_id, group_tid=group_id)
    if user.is_active:
        return
    context.bot.restrictChatMember(group_id, user_id, restricted_permissions)
    print(f"Restricted {user_id}")
    captcha, answer, buttons = captchaGenerator(user_id, group_id)
    markup = InlineKeyboardMarkup([buttons])
    name = update.message.from_user.first_name.replace('<', '&lt;').replace('>', '&gt;')
    message = f"درود {update.message.from_user.mention_html(name=name)},\n" \
        "جهت جلوگیری از ورود ربات‌ها، " \
        "دسترسی ارسال پیام از کاربران، " \
        "تا زمانی که خود را تایید نکنند گرفته می‌شود\n" \
        "جهت تایید کردن حساب‌کاربری خود، به معادله زیر پاسخ دهید\n" \
        f"<pre>{captcha} = ?</pre>\n" \
        "دکمه‌ای که پاسخ صحیح بر روی آن درج شده، انتخاب کنید."
    message = context.bot.sendMessage(group_id, message,
                                      reply_markup=markup,
                                      parse_mode=ParseMode.HTML)
    user.set_pending(message.message_id)
    context.bot.deleteMessage(group_id, update.message.message_id)


def checkAnswer(update, context):
    query = update.callback_query
    user_id, group_id, status = [int(value) for value in query.data.split(',')]
    if user_id != query.from_user.id:
        query.answer("❌ You can't activate someone else's account!")
        return
    if status != 1:
        query.answer("❌ Wrong Answer!")
        return
    user = User.get(user_tid=user_id, group_tid=group_id)
    user.activate()
    context.bot.restrictChatMember(group_id, user_id, unrestricted_permissions)
    user.save()
    query.answer("✅ You're account has been activated!")
    context.bot.deleteMessage(query.message.chat.id, query.message.message_id)


def err_handler(update, context):
    try:
        raise context.error
    except Exception as error:
        traceback.print_exc()


updater = Updater(TOKEN,
                  request_kwargs={'proxy_url': PROXY} if PROXY else None,
                  use_context=True)

updater.dispatcher.add_handler(
    MessageHandler(Filters.status_update.new_chat_members, kickBots)
)
updater.dispatcher.add_handler(
    MessageHandler(Filters.all, checkUser)
)
updater.dispatcher.add_handler(
    CallbackQueryHandler(checkAnswer)
)
updater.dispatcher.add_error_handler(err_handler)

logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)

if __name__ == "__main__":

    updater.start_polling()
    updater.idle()
