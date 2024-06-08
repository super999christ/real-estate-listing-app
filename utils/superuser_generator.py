from datetime import datetime

from config import Config

from crud.user import insert_user
from authentication.password_handler import hash_password


async def create_superuser() -> None:
    """Function for creating the superuser."""
    superuser = {
        'username': Config.SUPERUSER_USERNAME,
        'full_name': 'Arash Hajian nezhad',
        'email': Config.SUPERUSER_EMAIL,
        'password': hash_password(Config.SUPERUSER_PASSWORD),
        'date_of_birth': datetime(1998, 11, 20),
        'gender': 'MALE',
        'is_superuser': True,
        'created_at': datetime.utcnow(),
        'updated_at': datetime.utcnow(),
    }
        
    await insert_user(superuser)
