#!/usr/bin/env python3
"""create session authentication system"""

from typing import TypeVar
from api.v1.auth.auth import Auth
import uuid
from models.user import User


class SessionAuth(Auth):
    """class sesssion Auth inherits from Auth"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """creates a Session Id"""
        if user_id is None:
            return None
        if not isinstance(user_id, str):
            return None

        sessionID = str(uuid.uuid4())

        self.user_id_by_session_id[sessionID] = user_id
        return sessionID

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """returns a User ID based on session ID"""
        if session_id is None:
            return None
        if not isinstance(session_id, str):
            return None

        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None) -> TypeVar('User'):
        """returns a USER instance based on cookie value"""
        if request is None:
            return None

        session_cookie = self.session_cookie(request)
        user_ID = self.user_id_for_session_id(session_cookie)

        user = User.get(user_ID)
        return user

    def destroy_session(self, request=None):
        """deletes the user session/logout"""
        if request is None:
            return False

        session_cookie = self.session_cookie(request)
        if session_cookie is None:
            return False
        user_ID = self.user_id_for_session_id(session_cookie)
        if user_ID is None:
            return False
        del self.user_id_by_session_id[session_cookie]
        return True
