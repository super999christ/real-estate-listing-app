import os
from dotenv import load_dotenv
load_dotenv()

from fastapi import HTTPException


# read environment variables
jwt_secret = os.getenv('JWT_SECRET')
jwt_algorithm = os.getenv('JWT_ALGORITHM')
jwt_expiry_time = os.getenv('JWT_EXPIRY_TIME_IN_SECONDS')

db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')
db_name = os.getenv('DB_NAME')
db_username = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')

redis_host = os.getenv('REDIS_HOST')
redis_port = os.getenv('REDIS_PORT')
redis_db = os.getenv('REDIS_DB')

superuser_username = os.getenv('SUPERUSER_USERNAME')
superuser_password = os.getenv('SUPERUSER_PASSWORD')
superuser_email = os.getenv('SUPERUSER_EMAIL')

# boiler-plate error messages
error_message = {
    400: HTTPException(
        status_code=400,
        detail='Something went wrong / Bad request'
    ),
    401: HTTPException(
        status_code=401,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'}
    ),
    403: HTTPException(
        status_code=403,
        detail='Access Forbidden'
    ),
}


class Config:
    """
    Class for saving required configurations used in
    different parts of the app, all in one place.
    """
    DB_URL = f'postgresql+asyncpg://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}'
    
    JWT_SECRET = jwt_secret
    JWT_ALGORITHM = jwt_algorithm
    JWT_EXPIRY_TIME = int(jwt_expiry_time)

    REDIS_HOST = redis_host
    REDIS_PORT = int(redis_port)
    REDIS_DB = int(redis_db)

    SUPERUSER_USERNAME = superuser_username
    SUPERUSER_PASSWORD = superuser_password
    SUPERUSER_EMAIL = superuser_email

    RATE_LIMIT = 5
    RATE_LIMIT_EXPIRY_IN_SECONDS = 60
    
    API_PREFIX = '/api/v1'
    
    AUTH_PREFIX = '/auth'
    USERS_PREFIX = '/users'
    LISTINGS_PREFIX = '/listings'

    TOKEN_URL = API_PREFIX + AUTH_PREFIX + '/token/'
