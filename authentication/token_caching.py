from caching import redis_client
from config import Config, error_message


def store_token(token: str, user_id: str):
    """
    function for storing users tokens for limiting each
    user to be logged-in on one device-only at a time.
    """
    try:
        key = f'user_token:{user_id}'
        redis_client.set(key, token)
        redis_client.expire(key, Config.JWT_EXPIRY_TIME)
    except:
        raise error_message[400]


def revoke_token(user_id: str):
    """
    function for revoking a user's token, in cases
    like when the user changes their password, etc.
    """
    try:
        key = f'user_token:{user_id}'
        redis_client.delete(key)
    except:
        raise error_message[400]
