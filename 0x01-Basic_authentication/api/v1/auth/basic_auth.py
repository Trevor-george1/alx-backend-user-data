#!/usr/bin/env python3
"""Basic auth class that inherits from Auth"""

from api.v1.auth.auth import Auth
import base64


class BasicAuth(Auth):
    """basic auth class"""

    def extract_base64_authorization_header(self, authorization_header: str) -> str:  # Noqa
        """returns the BAse64 pasrt of authorization header"""
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith('Basic '):
            return None

        token = authorization_header.split(' ')[-1]
        return token

    def decode_base64_authorization_header(self, base64_authorization_header: str) -> str:  # Noqa
        "returns the header"
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None

        try:
            item_to_decode = base64_authorization_header.encode('utf-8')
            decoded = base64.b64decode(item_to_decode)
            return decoded.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(self, decoded_base64_authorization_header: str) -> (str, str):  # Noqa
        """returns the user email and password from base64 decoded"""
        if decoded_base64_authorization_header is None:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ':' in decoded_base64_authorization_header:
            email, password = decoded_base64_authorization_header.split(':')
            return email, password
        else:
            return None, None
