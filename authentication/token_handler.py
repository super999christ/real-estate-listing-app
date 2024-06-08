import time
from typing import Any
from jose import jwt, JWTError

from config import Config, error_message


secret = Config.JWT_SECRET
algorithm = Config.JWT_ALGORITHM
expiry_time = Config.JWT_EXPIRY_TIME


def create_token(payload: dict, expiry_time: float = expiry_time) -> str:
    """function for creating a new login token."""
    expiry_date = time.time() + expiry_time
    payload.update({'expiry_date': expiry_date})
    encoded_jwt = jwt.encode(payload, secret, algorithm=algorithm)
    return encoded_jwt


def decode_token(jwt_token: str) -> dict[str, Any]:
    """
    function for decoding a token
    for authentication purposes.
    """
    try:
        decoded_token = jwt.decode(jwt_token, secret, algorithms=[algorithm])
        if decoded_token['expiry_date'] >= time.time():
            return decoded_token
        raise error_message[401]
    except JWTError:
        raise error_message[401]
