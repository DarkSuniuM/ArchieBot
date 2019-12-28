"""
Models file.

Database instance and all of application models are defined here!
"""

import datetime as dt

from sqlalchemy.engine import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy import Column, Integer, Boolean, DateTime, UniqueConstraint, ForeignKey, BigInteger

from config import DB_URI


db = create_engine(DB_URI)
Base = declarative_base(db)
Session = sessionmaker(db)
session = Session()


class BaseModel:
    """Base Model.

    It's not an actual model, but all the models inherit this one.
    """
    id = Column(Integer, primary_key=True)

    @classmethod
    def get(cls, *args):
        return session.query(cls).filter(*args).first()

    @staticmethod
    def save():
        session.commit()


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
        self.is_active = True
        if self.pending:
            session.delete(self.pending)

    @classmethod
    def get_or_create(cls, user_tid, group_tid):
        """Get a user if exists, create it otherwise."""
        user = cls.get(user_tid, group_tid)

        if not user:
            user = cls()
            user.user_tid = user_tid
            user.group_tid = group_tid
            session.add(user)
            user.save()

        return user

    @classmethod
    def get(cls, user_tid, group_tid):
        user_tid_filter = cls.user_tid == user_tid
        group_tid_filter = cls.group_tid == group_tid
        return super().get(user_tid_filter, group_tid_filter)

    def set_pending(self, message_tid):
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
    message_tid = Column(Integer, nullable=False, unique=False, index=False)
    user = relationship('User', uselist=False, backref=backref('pending', uselist=False))

    @classmethod
    def get_or_create(cls, user_id, message_tid):
        pending = session.query(cls).filter(
            cls.user_id == user_id).first()

        if not pending:
            pending = cls()
            pending.user_id = user_id
            pending.message_tid = message_tid
            session.add(pending)
            pending.save()
        return pending
