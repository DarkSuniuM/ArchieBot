#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime as dt

from db.models import PendingUser, session
from bot import updater, UNRESTRICTED_PERMISSIONS


bot = updater.bot


def get_pending_users():
    """Get pending users.

    Get users who are not activated after 30 minutes.
    """
    now = dt.datetime.utcnow()
    _30_minutes_ago = now + dt.timedelta(minutes=-30)
    users = session.query(PendingUser).filter(PendingUser.create_date < _30_minutes_ago).all()
    return users


def unrestrict_temporary(user_tid, group_tid, message_tid):
    """Unrestrict user temporary and delete bot's activation message."""
    bot.restrictChatMember(group_tid, user_tid, UNRESTRICTED_PERMISSIONS)
    bot.deleteMessage(group_tid, message_tid)


if __name__ == "__main__":
    for pending in get_pending_users():
        unrestrict_temporary(pending.user.user_tid,
                             pending.user.group_tid,
                             pending.message_tid)
