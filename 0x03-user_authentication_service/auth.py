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
