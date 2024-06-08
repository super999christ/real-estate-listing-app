from fastapi import Request, Response

from config import Config
from caching import redis_client


rate = Config.RATE_LIMIT
rate_expiry = Config.RATE_LIMIT_EXPIRY_IN_SECONDS
token_path = Config.TOKEN_URL


async def limit_requests(request: Request, call_next) -> None | Response:
    """Function for limiting authentication requests based on settings in Config."""
    if request.url.path != token_path:  # no need to limit other requests, only login attempts
        return await call_next(request)

    ip = request.client.host
    key = f'user_ip:{ip}'
    request_count = redis_client.get(key)

    if request_count is None:
        redis_client.set(key, 1)
        redis_client.expire(key, rate_expiry)
    elif int(request_count) < rate:  # casting to `int` as Redis stores numbers as `bytes` type
        redis_client.incr(key)
    else:
        raise Response("Authentication Rate-Limit reached", status_code=403)
    
    response = await call_next(request)
    return response
