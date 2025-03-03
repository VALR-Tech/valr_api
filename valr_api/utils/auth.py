"""
Authentication utilities for VALR API
"""

import base64
import hashlib
import hmac
import json
import time
from typing import Dict, Optional, Union


def generate_signature(
    api_secret: str,
    timestamp: int,
    verb: str,
    path: str,
    body: Optional[Union[Dict, str]] = None,
) -> str:
    """
    Generate a signature for the VALR API request

    Args:
        api_secret: VALR API secret key
        timestamp: Unix timestamp in milliseconds
        verb: HTTP method (GET, POST, PUT, DELETE)
        path: API endpoint path
        body: Request body for POST/PUT requests

    Returns:
        Base64 encoded signature
    """
    # Create the payload string
    payload = str(timestamp) + verb.upper() + path

    # Add the request body if it exists
    if body:
        payload += json.dumps(body)

    # Create the signature
    message = payload.encode("utf-8")
    secret = api_secret.encode("utf-8")
    signature = hmac.new(secret, message, hashlib.sha512)

    # Return the base64 encoded signature
    return base64.b64encode(signature.digest()).decode("utf-8")


def get_timestamp() -> int:
    """
    Get current timestamp in milliseconds

    Returns:
        Current timestamp in milliseconds
    """
    return int(time.time() * 1000)
