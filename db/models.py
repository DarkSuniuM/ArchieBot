"""
Models file.

All database actual methods are defined here.
"""

import datetime as dt

from sqlalchemy import (BigInteger, Boolean, Column, ForeignKey, Integer,
                        UniqueConstraint, DateTime)
from sqlalchemy.orm import relationship, backref

from . import session, BaseModel, Base


class User(BaseModel, Base):
    """User Model."""

    __tablename__ = 'users'
    user_tid = Column(BigInteger,
                     nullable=False, unique=False, index=True)
    group_tid = Column(BigInteger,
                      nullable=False, unique=False, index=True)
    is_active = Column(Boolean,
                       nullable=False, unique=False, index=False,
                       default=False)
    __table_args__ = (UniqueConstraint('user_tid', 'group_tid'), )

    def activate(self):
        """Activate user."""
        self.is_active = True
        if self.pending:
            session.delete(self.pending)

    @classmethod
    def get_or_create(cls, user_tid, group_tid):
        """Get a user if exists, create it otherwise."""
        user = cls.get(user_tid, group_tid)

        if not user:
            user = cls.create(user_tid, group_tid)

        return user

    @classmethod
    def get(cls, user_tid, group_tid):
        """Get a user."""
        user_tid_filter = cls.user_tid == user_tid
        group_tid_filter = cls.group_tid == group_tid
        return super().get(user_tid_filter, group_tid_filter)

    @classmethod
    def create(cls, user_tid, group_tid):
        """Create a user."""
        user = cls()
        user.user_tid = user_tid
        user.group_tid = group_tid
        session.add(user)
        user.save()
        return user

    def set_pending(self, message_tid):
        """Set user status to pending."""
        pending = PendingUser.get_or_create(self.id, message_tid)
        pending.message_tid = message_tid
        pending.create_date = dt.datetime.utcnow()
        self.save()


class PendingUser(BaseModel, Base):
    """Pending User Model."""

    __tablename__ = 'pending_users'
    user_id = Column(Integer, ForeignKey('users.id'), unique=True)
    create_date = Column(DateTime,
                         nullable=False, unique=False, index=False,
                         default=dt.datetime.utcnow)
    message_tid = Column(Integer, nullable=True, unique=False, index=False)
    user = relationship('User', uselist=False, backref=backref('pending', uselist=False))

    @classmethod
    def get_or_create(cls, user_id, message_tid):
        """Get a pending user if exists, create it otherwise."""
        pending = cls.get(cls.user_id == user_id)

        if not pending:
            pending = cls.create(user_id, message_tid)
            
        return pending

    @classmethod
    def create(cls, user_id, message_tid):
        """Create a new pending user."""
        pending = cls()
        pending.user_id = user_id
        pending.message_tid = message_tid
        session.add(pending)
        pending.save()
        return pending
