import httpx
from cachetools import TTLCache, cached

from app.client.retry import retry

BASE_URL = "https://weisscrypto.com/en/api"


@cached(cache=TTLCache(maxsize=1, ttl=60 * 60 * 12))
@retry
def get_w50_history() -> httpx.Response:
    return httpx.get(f"{BASE_URL}/web/index-historical-chart/101")
