import datetime as dt
import logging
import time
from functools import wraps
from typing import Callable, Dict, List

import httpx


def retry(max_attempts: int = 3, asynchronous: bool = False) -> Callable:
    def wrapper(f: Callable) -> Callable:
        def handle_exception(e: httpx.HTTPStatusError):
            if e.response.status_code != 429:
                raise

            if "Retry-After" in e.response.headers:
                time_diff = dt.timedelta(seconds=int(e.response.headers["Retry-After"]))
            else:
                raise ValueError("No Retry-After headers found!")

            logging.getLogger().warning(
                "Too Many Requests. Sleeping for %d seconds...", time_diff.seconds
            )

            time.sleep(time_diff.seconds)

        @wraps(f)
        def caller_sync(*args: List, **kwargs: Dict) -> httpx.Response:
            for attempt in range(max_attempts):
                try:
                    return f(*args, **kwargs)
                except httpx.HTTPStatusError as e:
                    handle_exception(e)

        @wraps(f)
        async def caller_async(*args: List, **kwargs: Dict) -> httpx.Response:
            for attempt in range(max_attempts):
                try:
                    return await f(*args, **kwargs)
                except httpx.HTTPStatusError as e:
                    handle_exception(e)

        return caller_async if asynchronous else caller_sync

    return wrapper
