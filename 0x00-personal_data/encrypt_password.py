#!/usr/bin/env python3
"""
password Encyption and validation module
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """genrates a salted and hashed password"""
    encoded = password.encode()
    hashed = bcrypt.hashpw(encoded, bcrypt.gensalt())

    return hashed
