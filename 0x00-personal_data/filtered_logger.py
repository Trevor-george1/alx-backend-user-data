#!/usr/bin/env python3
"""
script for handling personal data
"""

from typing import List
import re
import logging
from os import environ



def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """
    Replaces sensitive information in a message with a redacted value
    based on the list of fields to reduct
    """
    for f in fields:
        message = re.sub(f"{f}=.*?{separator}",
                         f"{f}={redaction}{separator}", message)
    return message
