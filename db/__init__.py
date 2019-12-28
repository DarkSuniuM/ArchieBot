"""Database module main file."""

from sqlalchemy.engine import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer

from config import DB_URI

db = create_engine(DB_URI)
Base = declarative_base(db)
Session = sessionmaker(db)
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
