import datetime as dt
import logging
import time
from functools import wraps
from typing import Callable, Dict, List

import httpx

_RESET_FORMAT = "%Y-%m-%d %H:%M:%S %z"


def retry(f: Callable) -> Callable:
    @wraps(f)
    def caller(*args: List, **kwargs: Dict) -> httpx.Response:
        def make_call() -> httpx.Response:
            return f(*args, **kwargs)

        while True:
            try:
                result = make_call()
            except httpx.HTTPStatusError as e:
                if e.response.status_code != 429:
                    raise

                time_diff = (
                    dt.datetime.strptime(
                        e.response.headers["X-RateLimit-Reset"], _RESET_FORMAT
                    )
                    - dt.datetime.now().astimezone()
                )
                logging.getLogger().warning(
                    "Too Many Requests. Sleeping for %d seconds...", time_diff.seconds
                )
                time.sleep(time_diff.seconds)

            else:
                return result

    return caller
