"""
Utils file.

Functions that are getting used by
direct handlers are defined here!
"""
import re
import requests
import datetime as dt
from telegram import InlineKeyboardButton, ChatMember
from telegram.error import BadRequest
from random import randint, sample, shuffle

from db import session
from db.models import PendingUser

from . import UNRESTRICTED_PERMISSIONS


def captcha_generator(user_id, group_id):
    """Generate captcha."""
    first_operator = 2
    second_operator = randint(1, 10)
    correct_answer = first_operator * second_operator
    equation = f"{first_operator} * {second_operator}"
    all_answers = answer_generator(correct_answer, 4)
    inline_buttons = []
    for answer in all_answers:
        data = f"{user_id},{group_id},{int(answer == correct_answer) or -answer}"
        button = InlineKeyboardButton(answer, callback_data=data)
        inline_buttons.append(button)
    return (equation, correct_answer, inline_buttons)


def answer_generator(correct_answer, length):
    """Generate captcha answers."""
    first_list = list(range(0, correct_answer))
    second_list = list(range(correct_answer + 1, length))
    random_generated_list = sample(first_list + second_list, length - 1)
    random_generated_list.append(correct_answer)
    shuffle(random_generated_list)
    return random_generated_list


def is_admin(bot, chat_id, user_id):
    """Check if user is admin in the given chat or not."""
    chat_member = bot.get_chat_member(chat_id, user_id)
    ADMIN_GROUPS = (ChatMember.ADMINISTRATOR, ChatMember.CREATOR)
    if chat_member.status in ADMIN_GROUPS:
        return True
    return False


def get_pending_users(seconds):
    """Get pending users.

    Get users who are not activated after specified time.
    """
    now = dt.datetime.utcnow()
    seconds_ago = now - dt.timedelta(seconds=seconds)
    users = session.query(PendingUser) \
                   .filter(
                       PendingUser.message_tid != None,
                       PendingUser.create_date < seconds_ago
                    ) \
                   .all()
    return users


def unrestrict_temporary(bot, user_tid, group_tid, message_tid):
    """Unrestrict user temporary and delete bot's activation message."""
    bot.restrictChatMember(group_tid, user_tid, UNRESTRICTED_PERMISSIONS)
    try:
        bot.deleteMessage(group_tid, message_tid)
    except BadRequest:
        pass


def mark_pending_deleted(pending_user):
    """Mark a pending message as deleted."""
    pending_user.message_tid = None
    pending_user.save()


def search_wiki(search_query):
    """Search within the Archlinux Wiki."""
    results = []

    if not search_query:
        return results

    english_request = requests.get(
        f'https://wiki.archlinux.org/api.php?action=opensearch&search={search_query}',
        timeout=2)
    persian_request = requests.get(
        f'https://wiki.archusers.ir/api.php?action=opensearch&search={search_query}',
        timeout=2)

    englush_results = english_request.json() if english_request.status_code == 200 else {}
    persian_results = persian_request.json() if persian_request.status_code == 200 else {}

    for i, result in enumerate(englush_results[1]):
        if not '(' in result:
            results.append({
                'title': result,
                'url': englush_results[3][i]
            })

    for i, result in enumerate(persian_results[1]):
        results.append({'title': f'{result} (Persian)', 'url': persian_results[3][i]})

    return results