import random
from datetime import datetime

from faker import Faker

from crud.user import bulk_insert_users
from authentication.password_handler import hash_password


async def generate_fake_users(n: int = 3) -> dict[str, str]:
    """Function for generating and inserting `n` new fake members."""
    fake = Faker()
    fakes = []

    for _ in range(n):
        fake_user = {
            'username': fake.user_name(),
            'full_name': fake.name(),
            'email': fake.email(),
            'password': hash_password(fake.password()),  # hashing the passwords take so long!
            'date_of_birth': fake.date_between_dates(date_start=datetime(1941,1,1), date_end=datetime(2000,12,31)),
            'gender': random.choice(['MALE', 'FEMALE', 'NOT_SPECIFIED']),
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow(),
        }

        fakes.append(fake_user)
    
    await bulk_insert_users(fakes)
    return {'RandomUsersGenerated': f'{n} random users were succesfully generated'}
