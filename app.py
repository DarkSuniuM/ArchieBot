from random import randint, sample, shuffle

import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import CallbackQueryHandler, Filters, MessageHandler, Updater

from config import PROXY, TOKEN
from models import User


def captchaGenerator(user_id, group_id):
    first_operator = 2
    second_operator = randint(1, 10)
    correct_answer = first_operator * second_operator
    equation = f"{first_operator} * {second_operator}"
    all_answers = answerGenerator(correct_answer, 4)
    inline_buttons = []
    for answer in all_answers:
        data = f"{user_id},{group_id},{answer == correct_answer}"
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


def kickBots(bot, update):
    for new_user in update.message.new_chat_members:
        if new_user.is_bot and new_user.id != bot.id:
            bot.kickChatMember(update.message.chat.id, new_user.id, timeout=5)
        if not new_user.is_bot:
            checkUser(bot, update)


def checkUser(bot, update):
    group_id = update.message.chat.id
    user_id = update.message.from_user.id
    if user_id == bot.id:
        return
    user, created = User.get_or_create(user_id=user_id, group_id=group_id)
    if user.is_active:
        return
    bot.restrictChatMember(group_id, user_id, can_send_messages=0)
    captcha, answer, buttons = captchaGenerator(user_id, group_id)
    markup = InlineKeyboardMarkup([buttons])
    message = f"درود {update.message.from_user.mention_markdown()},\n" \
        "جهت جلوگیری از ورود ربات‌ها،" \
        "دسترسی ارسال پیام از کاربران،" \
        "تا زمانی که خود را تایید نکنند گرفته می‌شود\n" \
        "جهت تایید کردن حساب‌کاربری خود، به معادله زیر پاسخ دهید\n" \
        f"`{captcha} = ?`\n" \
        "دکمه‌ای که پاسخ صحیح بر روی آن ردج شده، انتخاب کنید."
    bot.sendMessage(group_id, message,
                    reply_markup=markup, parse_mode=ParseMode.MARKDOWN)
    bot.deleteMessage(group_id, update.message.message_id)


def checkAnswer(bot, update):
    query = update.callback_query
    user_id, group_id, status = [int(value) for value in query.data.split(',')]
    if user_id != query.from_user.id:
        query.answer("❌ You can't activate someone else's account!")
        return
    if not status:
        query.answer("❌ Wrong Answer!")
        return
    user = User.get(user_id=user_id, group_id=group_id)
    user.is_active = 1
    bot.restrictChatMember(group_id, user_id, can_send_messages=1)
    user.save()
    query.answer("✅ You're account has been activated!")
    bot.deleteMessage(query.message.chat.id, query.message.message_id)


def err_handler(bot, update, error):
    try:
        raise error
    except Exception:
        pass


updater = Updater(TOKEN,
                  request_kwargs={'proxy_url': PROXY} if PROXY else None)

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

updater.start_polling()
updater.idle()
