"""Bot Handlers.

All bot handlers are defined here!
"""

import datetime as dt
import traceback as tb

from telegram import ChatPermissions, InlineKeyboardMarkup, ParseMode

from db.models import User

from . import RESTRICTED_PERMISSIONS, UNRESTRICTED_PERMISSIONS
from .utils import captcha_generator

def check_user(update, context):
    """Check if a user can send message or not."""
    group_id = update.message.chat.id
    user_id = update.message.from_user.id
    message_time = update.message.date.timestamp()
    bot = context.bot

    CONDITIONS = ( # Ignore if 
        user_id == 777000,  # User is official message migrate account,
        message_time + 3 < dt.datetime.utcnow().timestamp(),  # Message older than 3 secs,
        user_id == bot.id  # User is the bot itself
    )
    if any(CONDITIONS):
        return

    user = User.get_or_create(user_tid=user_id, group_tid=group_id)
    if user.is_active:
        return

    bot.restrictChatMember(group_id, user_id, RESTRICTED_PERMISSIONS)
    captcha, answer, buttons = captcha_generator(user_id, group_id)
    markup = InlineKeyboardMarkup([buttons])
    name = update.message.from_user.first_name.replace('<', '&lt;').replace('>', '&gt;')
    message = f"درود {update.message.from_user.mention_html(name=name)},\n" \
        "جهت جلوگیری از ورود ربات‌ها، " \
        "دسترسی ارسال پیام از کاربران، " \
        "تا زمانی که خود را تایید نکنند گرفته می‌شود\n" \
        "جهت تایید کردن حساب‌کاربری خود، به معادله زیر پاسخ دهید\n" \
        f"<pre>{captcha} = ?</pre>\n" \
        "دکمه‌ای که پاسخ صحیح بر روی آن درج شده، انتخاب کنید."
    message = bot.sendMessage(group_id, message, reply_markup=markup,
                              parse_mode=ParseMode.HTML)
    user.set_pending(message.message_id)
    bot.deleteMessage(group_id, update.message.message_id)


def kick_bots(update, context):
    """Kick new members who are identified as bot."""
    for new_user in update.message.new_chat_members:
        if new_user.is_bot and new_user.id != context.bot.id:
            context.bot.kickChatMember(update.message.chat.id, new_user.id, timeout=5)
        if not new_user.is_bot:
            check_user(update, context)


def check_answer(update, context):
    """Check if the answer is right or not."""
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
    context.bot.restrictChatMember(group_id, user_id, UNRESTRICTED_PERMISSIONS)
    user.save()
    query.answer("✅ You're account has been activated!")
    context.bot.deleteMessage(query.message.chat.id, query.message.message_id)


def error_handler(update, context):
    """Handle error."""
    try:
        raise context.error
    except Exception as error:
        tb.print_exc()
