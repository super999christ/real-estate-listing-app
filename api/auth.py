from datetime import datetime

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from config import Config, error_message

from crud.user import (
    insert_user,
    fetch_user_by_username,
    check_if_username_exists,
    check_if_email_exists,
)

from schemas import UserSignup

from authentication.password_handler import hash_password
from authentication.token_handler import create_token
from authentication.token_caching import store_token
from authentication.authentication_handler import authenticate_user


auth = APIRouter(prefix=Config.AUTH_PREFIX)


@auth.post('/signup/', tags=['Authentication'])
async def user_signup(user: UserSignup) -> dict[str, str]:
    """Register a new user."""
    current_time = datetime.utcnow()
    
    if await check_if_username_exists(user.username):
        return {'UsernameError': 'This username is already taken / Pick another one'}

    if await check_if_email_exists(user.email):
        return {'EmailError': 'This email has already signed up / Use another one'}

    user.password = hash_password(user.password)
    user = user.dict()
    user.update({
        'created_at': current_time,
        'updated_at': current_time,
    })
    response = await insert_user(user)
    if response:
        return response
    raise error_message[400]


@auth.post('/token/', tags=['Authentication'])
async def user_login(form: OAuth2PasswordRequestForm = Depends()) -> dict[str, str]:
    """Obtain a new login token."""
    if await authenticate_user(form.username, form.password):
        user = await fetch_user_by_username(form.username)
        user_id = user.get('id')
        payload = {'sub': user_id}
        print(f'[LOGIN] user \033[1m{form.username}\033[0m has successfully logged in')

        # fetching the access token and saving it inside Redis
        access_token = create_token(payload)
        store_token(access_token, user_id)
        return {'access_token': access_token, 'token_type': 'Bearer'}
    raise error_message[401]
