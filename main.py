from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from api.auth import auth
from api.user import users
from api.listing import listings

from config import Config
from database import db

from crud.user import is_superuser_registered
from utils.count import count_startup
from utils.logging import log_request
from utils.rate_limit import limit_requests
from utils.fake_generator import generate_fake_users
from utils.superuser_generator import create_superuser


app = FastAPI(
    title='Dornica Real Estate API',
    description='A Real Estate app as an assessment test for back-end role at Dornica.',
    version='1.0',
)

# adding middlewares
origins = [
    'http://localhost:3000',
]

# adding CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# adding logging middleware
@app.middleware('http')
async def log_middleware(request: Request, call_next) -> None:
    """auxilliary function for calling the main logging function"""
    return await log_request(request, call_next)


# adding authentication rate-limit middleware
@app.middleware('http')
async def ratelimit_middleware(request: Request, call_next) -> None:
    """auxilliary function for calling the main rate-limit function"""
    return await limit_requests(request, call_next)


@app.on_event('startup')
async def startup():
    """Startup function for specifying the actions done at the application startup."""
    # count the startup
    count_startup()
    await db.create_all()

    # create superuser
    if await is_superuser_registered() is not True:
        await create_superuser()
        print('[SUPERUSER] The superuser was successfully created')
    
    # create 3 random users
    await generate_fake_users(n=3)


@app.on_event('shutdown')
async def shutdown():
    """Shutdown function for specifying the actions done at the application shutdown."""
    await db.close()


@app.get('/', tags=['Homepage'])
async def homepage():
    """Homepage endpoint, nothing to see here."""
    return {'Message': 'Welcome to the homepage'}


# adding the API routes specified inside the `api` folder
app.include_router(auth, prefix=Config.API_PREFIX)
app.include_router(users, prefix=Config.API_PREFIX)
app.include_router(listings, prefix=Config.API_PREFIX)
