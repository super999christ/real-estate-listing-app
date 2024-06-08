from jose import jwt, JWTError

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from config import Config, error_message
from schemas import UserLogin
from caching import redis_client
from crud.user import fetch_user_by_username, fetch_user_by_id
from authentication.password_handler import verify_password


oauth2_scheme = OAuth2PasswordBearer(tokenUrl=Config.TOKEN_URL)
secret = Config.JWT_SECRET
algorithm = Config.JWT_ALGORITHM

rate = Config.RATE_LIMIT
rate_expiry = Config.RATE_LIMIT_EXPIRY_IN_SECONDS


async def authenticate_user(username: str, password: str) -> bool:
    """function for checking user's credentials."""
    user_in_database = await fetch_user_by_username(username)
    if user_in_database.get('NoUsersFoundError') is not None:
        raise error_message[401]

    user_in_database = UserLogin(**user_in_database)
    if verify_password(password, user_in_database.password) == False:
        raise error_message[401]
    
    return True


async def get_current_user(token: str = Depends(oauth2_scheme)) -> dict[str, str]:
    """function for extracting the user of the token."""
    try:
        payload = jwt.decode(token, secret, algorithms=[algorithm])
        user_id = payload.get('sub')
        if user_id is None:
            raise error_message[401]

        # checking if the token exists inside the redis database
        key = f'user_token:{user_id}'
        stored_token = redis_client.get(key)
        if stored_token is None or stored_token.decode() != token:
            raise error_message[401]
    except JWTError:
        raise error_message[401]

    user = await fetch_user_by_id(user_id)
    if user.get('NoUsersFoundError') is not None:
        raise error_message[401]

    return user['id']
