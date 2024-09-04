#!/usr/bin/env python3
"""create session authentication system"""

from api.v1.auth.auth import Auth
import uuid


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
