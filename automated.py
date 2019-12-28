#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime as dt

from models import PendingUser, session
from app import updater, unrestricted_permissions


bot = updater.bot


def getPendingUsers():
    now = dt.datetime.utcnow()
    _30_minutes_ago = now + dt.timedelta(minutes=-1)
    print(_30_minutes_ago)

    users = session.query(PendingUser).filter(PendingUser.create_date < _30_minutes_ago).all()
    return users


def unrestrictTemporary(user_tid, group_tid, message_tid):
    bot.restrictChatMember(group_tid, user_tid, unrestricted_permissions)
    bot.deleteMessage(group_tid, message_tid)


if __name__ == "__main__":
    for pending in getPendingUsers():
        print(pending)
        unrestrictTemporary(pending.user.user_tid, pending.user.group_tid, pending.message_tid)
