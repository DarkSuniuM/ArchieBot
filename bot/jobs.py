"""
Scheduled jobs.

All scheduled jobs are defined here!
"""
from .utils import get_pending_users, unrestrict_temporary, mark_pending_deleted


def delete_pending_activation_messages(context):
    """Delete pending messages from bot after a specified time."""
    for pending in get_pending_users(10):
        unrestrict_temporary(context.bot,
                             pending.user.user_tid,
                             pending.user.group_tid,
                             pending.message_tid)
        mark_pending_deleted(pending)
