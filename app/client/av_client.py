import httpx
from cachetools import TTLCache, cached

from app.client.retry import retry
from app.config import Config

FULL_URL = "https://www.alphavantage.co/query"


@cached(cache=TTLCache(maxsize=128, ttl=60 * 60 * 12))
@retry
def get_daily_market_chart(symbol: str) -> httpx.Response:
    response = httpx.get(
        url=FULL_URL,
        params={
            "function": "TIME_SERIES_DAILY",
            "symbol": symbol,
            "outputsize": "full",
            "datatype": "json",
            "apikey": Config.alpha_vantage_key,
        },
    )
    response.raise_for_status()
    return response
