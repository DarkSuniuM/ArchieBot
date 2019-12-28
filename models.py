"""
Models file.

Database instance and all of application models are defined here!
"""

import datetime as dt

from sqlalchemy.engine import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, Boolean, DateTime, UniqueConstraint

from config import DB_URI


db = create_engine(DB_URI)
Base = declarative_base(db)
Session = sessionmaker(db)


def session():
    """Create a database session."""
    return Session()


class User(Base):
    """User Model."""

    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer,
                     nullable=False, unique=False, index=True)
    group_id = Column(Integer,
                      nullable=False, unique=False, index=True)
    is_active = Column(Boolean,
                       nullable=False, unique=False, index=False,
                       default=False)
    create_date = Column(DateTime,
                         nullable=False, unique=False, index=False,
                         default=dt.datetime.utcnow)
    __table_args__ = (UniqueConstraint('user_id', 'group_id'), )
