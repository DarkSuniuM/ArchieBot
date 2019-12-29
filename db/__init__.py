"""Database module main file."""

from sqlalchemy.engine import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import Column, Integer

from config import DB_URI

db = create_engine(DB_URI, convert_unicode=True, connect_args=dict(use_unicode=True))
Base = declarative_base(db)
session_factory = sessionmaker(db)
Session = scoped_session(session_factory)
session = Session()


class BaseModel:
    """
    Base Model.

    It's not an actual model, but all the models inherit this one.
    """

    id = Column(Integer, primary_key=True)

    @classmethod
    def get(cls, *args):
        """Get an object."""
        return session.query(cls).filter(*args).first()

    @staticmethod
    def save():
        """Commit changes to database."""
        session.commit()
