from fastapi import Request
from datetime import datetime


async def log_request(request: Request, call_next) -> None:
    """Function for logging every request's IP address and exact time."""
    with open('logs.txt', 'a') as file:
        file.write(f'[TIME] {datetime.utcnow()}  -  [IP] {request.client.host}\n')
    response = await call_next(request)
    return response
