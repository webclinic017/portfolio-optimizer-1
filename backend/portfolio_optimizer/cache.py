from functools import wraps
from typing import Any, Callable, Collection

import requests_cache


def use_requests_cache(
    cache_name: str = "main_http_cache", expiry: int = 60 * 60
) -> Callable:
    def wrap_function(f: Callable) -> Any:
        @wraps(f)
        def wrapper(*args: Collection, **kwargs: Collection) -> Any:
            with requests_cache.enabled(
                cache_name, expire_after=expiry, backend="memory"
            ):
                return f(*args, **kwargs)

        return wrapper

    return wrap_function
