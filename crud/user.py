from uuid import uuid4

from sqlalchemy import insert, update, delete
from sqlalchemy.future import select

from models import User
from database import db, transaction

from utils.bulk_query_handler import bulk_query_to_dict


async def fetch_all_users() -> list[dict[str, str]]:
    """Fetch all users from the database."""
    query = select(User)
    users = await db.execute(query)
    users = users.scalars().all()
    if not users:
        return [{'NoUsersFoundError': 'No users are registered'}]
    return bulk_query_to_dict(users)


async def fetch_user_by_username(username: str) -> dict[str, str]:
    """Fetch a certain user by their username from the database."""
    query = select(User).where(User.username == username)
    user = await db.execute(query)
    user = user.scalar()
    if user:
        user = user.__dict__
        return user
    return {'NoUsersFoundError': 'No user was found with this username'}


async def fetch_user_by_id(id: str) -> dict[str, str]:
    """Fetch a certain user by their id from the database."""
    query = select(User).where(User.id == id)
    user = await db.execute(query)
    user = user.scalar()
    if user:
        user = user.__dict__
        return user
    return {'NoUsersFoundError': 'No user was found with this id'}


async def check_if_username_exists(username: str) -> bool:
    """Check if the username is already being used by another user inside the database."""
    query = select(User).where(User.username == username)
    user = await db.execute(query)
    if user.scalar() is not None:
        return True
    return False


async def check_if_email_exists(email: str) -> bool:
    """Check if the email is already registered inside the database."""
    query = select(User).where(User.email == email)
    user = await db.execute(query)
    if user.scalar():
        return True
    return False


async def insert_user(user: dict) -> dict[str, dict[str, str]]:
    """Insert a new user inside the database"""
    user.update({'id': uuid4().hex})  # first add a new random ID to the user values
    stmt = insert(User).values(**user)
    await db.execute(stmt)

    user.pop('password')  # remove the password data and do not show it
    return await transaction(msg=f'User successfully registered: {user}')


async def bulk_insert_users(users: list[dict]) -> dict[str, str]:
    """Insert a bulk of new users inside the database (for fake users generation)."""
    for idx in range(len(users)):
        users[idx].update({'id': uuid4().hex})
    stmt = insert(User).values(users)
    await db.execute(stmt)
    return await transaction(msg='New users were successfully registered.')


async def is_superuser_registered() -> bool:
    """Check if there exists at least one superuser inside the database."""
    query = select(User).where(User.is_superuser == True)
    user = await db.execute(query)
    user = user.scalar()
    if user:
        return True
    return False


async def update_password(id: str, new_password: str) -> dict[str, str]:
    """Update the password of a certain user by their id inside the database."""
    stmt = (
        update(User)
        .where(User.id == id)
        .values(password=new_password)
        .execution_options(synchronize_session='fetch')
    )

    await db.execute(stmt)
    return await transaction(msg='Password succesfully changed')


async def update_user(id: str, **kwargs) -> dict[str, str]:
    """Update a user by their id with new information inside the database."""
    stmt = (
        update(User)
        .where(User.id == id)
        .values(**kwargs)
        .execution_options(synchronize_session='fetch')
    )

    await db.execute(stmt)
    return await transaction(msg='User successfully updated')


async def delete_user(id: str) -> dict[str, dict[str, str] | str]:
    """Delete a user by their id from the database."""
    stmt = delete(User).where(User.id == id).returning(User.id, User.username)
    affected_row = await db.execute(stmt)
    affected_row = affected_row.first()

    if affected_row is not None:
        return await transaction(f'User successully deleted: {affected_row}')
    return {'NoUsersFoundError': 'No user was found with this id'}


async def delete_all_users() -> dict[str, str]:
    """Delete all of the registered users, except the `superusers`, from the database."""
    stmt = delete(User).where(User.is_superuser == False).returning(User.id, User.username)
    affected_row = await db.execute(stmt)
    affected_row = affected_row.first()

    if affected_row:
        return await transaction(f'All users successully deleted')
    return {'NoUsersFoundError': 'No user has been registered yet'}
