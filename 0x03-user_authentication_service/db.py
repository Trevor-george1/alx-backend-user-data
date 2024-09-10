#!/usr/bin/env python3
"""DB module
"""
import logging
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound

from user import Base, User


logging.getLogger('sqlalchemy').setLevel(logging.CRITICAL)
logging.getLogger('sqlalchemy.engine').setLevel(logging.CRITICAL)
logging.getLogger('sqlalchemy.pool').setLevel(logging.CRITICAL)
logging.getLogger('sqlalchemy.dialects.sqlite.base').setLevel(logging.CRITICAL)


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """saves the user to the database"""
        new_user = User(email=email, hashed_password=hashed_password)

        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """return a user based on the given arguments"""
        if not kwargs:
            raise InvalidRequestError

        user = self._session.query(User).filter_by(**kwargs).first()

        if not user:
            raise NoResultFound

        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """updates a user using kwargs"""
        user = self.find_user_by(id=user_id)
        for key, value in kwargs.items():
            if not hasattr(user, key):
                raise ValueError
            else:
                setattr(user, key, value)

        self._session.commit()
        return None
