from redis import Redis
from config import Config


# Redis client used for caching required data
redis_client = Redis(
    host=Config.REDIS_HOST,
    port=Config.REDIS_PORT,
    db=Config.REDIS_DB,
)
