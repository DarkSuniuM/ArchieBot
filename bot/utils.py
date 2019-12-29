"""
Utils file.

Functions that are getting used by
direct handlers are defined here!
"""
import datetime as dt
from random import randint, sample, shuffle

from telegram import InlineKeyboardButton

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
    bot.deleteMessage(group_tid, message_tid)


def mark_pending_deleted(pending_user):
    """Mark a pending message as deleted."""
    pending_user.message_tid = None
    pending_user.save()
