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


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    validates whether the provided password matches the hashed password
    """
    valid = False
    encoded = password.encode()
    if bcrypt.checkpw(encoded, hashed_password):
        valid = True
    return valid
