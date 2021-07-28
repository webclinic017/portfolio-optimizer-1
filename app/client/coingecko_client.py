from typing import Union

import httpx
from cachetools import TTLCache, cached

from app.client.retry import retry

BASE_URL = "https://api.coingecko.com/api/v3"


@cached(cache=TTLCache(maxsize=1, ttl=60 * 60 * 12))
@retry
def get_search() -> httpx.Response:
    """
    A hidden endpoint which returns all coins and relative information.
    :return: httpx.Response
    """
    response = httpx.get(url=f"{BASE_URL}/search")
    response.raise_for_status()
    return response


@cached(cache=TTLCache(maxsize=128, ttl=60 * 60 * 12))
@retry
def get_daily_market_chart(
    coin: str, days: Union[int, str, None] = None
) -> httpx.Response:
    response = httpx.get(
        url=f"{BASE_URL}/coins/{coin}/market_chart",
        params={"vs_currency": "usd", "days": days or "max", "interval": "daily"},
    )
    response.raise_for_status()
    return response
