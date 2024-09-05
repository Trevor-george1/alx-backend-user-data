#!/usr/bin/env python3
"""a class to manage the API application"""

from flask import request
import os
from typing import List, TypeVar


class Auth():
    """class AUth"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """return false"""
        if path is None:
            return True
        if excluded_paths == [] or excluded_paths is None:
            return True
        if path in excluded_paths:
            return False
        for p in excluded_paths:
            if p.startswith(path):
                return False
            elif path.startswith(p):
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """auth header"""
        if request is None:
            return None

        header = request.headers.get("Authorization")

        if header is None:
            return None

        return header

    def current_user(self, request=None) -> TypeVar('User'):
        """current user"""
        return None

    def session_cookie(self, request=None):
        """returns a cookie value from a request"""
        if request is None:
            return None

        session_name = os.getenv("SESSION_NAME")
        cookie = request.cookies.get(session_name)
        return cookie
