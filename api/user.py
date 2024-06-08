from datetime import datetime

from fastapi import APIRouter, Depends

from config import Config, error_message
from crud.user import (
    delete_all_users,
    fetch_user_by_id,
    fetch_user_by_username,
    fetch_all_users,
    update_password,
    update_user,
    delete_user,
)
from schemas import UserUpdate, UserView
from authentication.password_handler import hash_password, verify_password
from authentication.authentication_handler import get_current_user
from authentication.token_caching import revoke_token
from utils.fake_generator import generate_fake_users


users = APIRouter(prefix=Config.USERS_PREFIX)


@users.get('/getUser/', tags=['User'], response_model=UserView | dict[str, str])
async def get_user_by_username(username: str, user_id: str = Depends(get_current_user)) -> dict[str, str]:
    """[SUPERUSER-ONLY] Get a user's info by its username."""
    current_user = await fetch_user_by_id(user_id)
    if current_user.get('is_supermodel') == False:
        raise error_message[403]
    
    response = await fetch_user_by_username(username)
    if response:
        return response
    raise error_message[400]


@users.get('/getAllUsers/', tags=['User'], response_model=list[UserView] | list[dict[str, str]])
async def get_all_users(user_id: str = Depends(get_current_user)) -> list[dict[str, str]]:
    """[SUPERUSER-ONLY] Get all registered users' info."""
    current_user = await fetch_user_by_id(user_id)
    if current_user.get('is_supermodel') == False:
        raise error_message[403]

    response = await fetch_all_users()
    if response:
        return response
    raise error_message[400]


@users.post('/generateFakeUsers/', tags=['User'])
async def generate_random_users(user_id: str = Depends(get_current_user), n: int = 3) -> dict[str, str]:
    """[SUPERUSER-ONLY] Inserts `n` random fake users."""
    current_user = await fetch_user_by_id(user_id)
    if current_user.get('is_supermodel') == False:
        raise error_message[403]
    
    response = await generate_fake_users(n=n)
    if response:
        return response
    raise error_message[400]


@users.put('/updatePassword/', tags=['User'])
async def edit_password(old_password: str, new_password: str, user_id: str = Depends(get_current_user)) -> dict[str, str]:
    """Edit the current logged-in user's password."""
    if not old_password or not new_password:
        return {'EmptyFieldsError': 'You must fill both the new password field and the old password field'}
    
    user = await fetch_user_by_id(user_id)
    password_in_database = user.get('password')
    
    if not verify_password(old_password, password_in_database):
        return {'PasswordError': 'Current password is incorrect'}
    
    if old_password == new_password:
        return {'PasswordError': 'The new password entered is same as the current password; Enter a new one'}
    
    new_password = hash_password(new_password)
    response = await update_password(user_id, new_password)
    if response:
        # we should revoke the current token
        revoke_token(user_id)
        return response
    raise error_message[400]


@users.put('/updateUser/', tags=['User'])
async def edit_user(user: UserUpdate, user_id: str = Depends(get_current_user)) -> dict[str, str]:
    """Edit the current logged-in user's info."""
    user = {key: value for key, value in user.dict().items() if value != '' and value != None}
    user.update({'updated_at': datetime.utcnow()})

    response = await update_user(user_id, **user)
    if response:
        return response
    raise error_message[400]


@users.delete('/deleteUser/', tags=['User'])
async def remove_user(user_id: str = Depends(get_current_user)) -> dict[str, str]:
    """Delete the current logged-in user's account."""
    response = await delete_user(user_id)
    if response:
        return response
    raise error_message[400]


@users.delete('/deleteAllUsers/', tags=['User'])
async def remove_all_users(user_id: str = Depends(get_current_user)) -> dict[str, str]:
    """[SUPERUSER-ONLY] Delete every registered user."""
    current_user = await fetch_user_by_id(user_id)
    if current_user.get('is_supermodel') == False:
        raise error_message[403]

    response = await delete_all_users()
    if response:
        return response
    raise error_message[400]
