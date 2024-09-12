#!/usr/bin/env python3
"""_hash

-password that hashes a password and returns bytes"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from typing import Union
import uuid


def _hash_password(password: str) -> bytes:
    """returns bytes"""

    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt)


def _generate_uuid() -> str:
    """returns a string representation of new UUID"""
    id = uuid.uuid4()
    return str(id)


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> Union[None, User]:
        """register a new user, if user already exists don't create"""
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:

            return self._db.add_user(email, _hash_password(password))
        else:
            raise ValueError('User {} already exists'.format(email))

    def valid_login(self, email: str, password: str) -> bool:
        """returns True or false"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False

        return bcrypt.checkpw(password.encode('utf-8'), user.hashed_password)

    def create_session(self, email: str) -> str:
        """returns the session ID as string"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        user.session_id = _generate_uuid()
        return user.session_id

    def get_user_from_session_id(self, session_id: str) -> User:
        """takes session id and returns a user"""
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None
        else:
            return user

    def destroy_session(self, user_id: int) -> None:
        """destory a session by clearing the session_id"""
        try:
            user = self._db.find_user_by(user_id=user_id)
        except NoResultFound:
            return None
        else:
            user.session_id = None
