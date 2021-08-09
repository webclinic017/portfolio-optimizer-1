import datetime as dt
from typing import Dict, List, Optional, Union

from cachetools import TTLCache, cached
from coingecko_api_client.client import CoinGeckoAPIAsyncClient
from utils import coingecko_retry

_client: CoinGeckoAPIAsyncClient = CoinGeckoAPIAsyncClient()


async def close() -> None:
    await _client.close()


@cached(cache=TTLCache(maxsize=128, ttl=60 * 60 * 24))
@coingecko_retry.retry(asynchronous=True)
async def get_top_coins(
    vs_currency: str,
    ids: Optional[List[str]] = None,
    category: Optional[str] = None,
    order: str = "market_cap_desc",
    per_page: int = 100,
    page: int = 1,
    sparkline: bool = False,
    price_change_percentage: Optional[List[str]] = None,
) -> List[str]:
    coins_markets = await _client.coins_markets(
        vs_currency=vs_currency,
        ids=ids,
        category=category,
        order=order,
        per_page=per_page,
        page=page,
        sparkline=sparkline,
        price_change_percentage=price_change_percentage,
    )
    return [c["id"] for c in coins_markets]


@cached(cache=TTLCache(maxsize=128, ttl=60 * 60 * 24))
@coingecko_retry.retry(asynchronous=True)
async def get_coin_market_chart(
    coin_id: str,
    vs_currency: str,
    days: Union[int, str] = "max",
    interval: str = "daily",
) -> Dict[str, Dict[dt.date, float]]:
    coin_market_chart = await _client.coin_market_chart(
        coin_id=coin_id, vs_currency=vs_currency, days=days, interval=interval
    )
    return {
        "prices": {
            dt.date.fromtimestamp(ts / 1000): price
            for ts, price in coin_market_chart["prices"]
        },
        "market_caps": {
            dt.date.fromtimestamp(ts / 1000): market_cap
            for ts, market_cap in coin_market_chart["market_caps"]
        },
        "total_volumes": {
            dt.date.fromtimestamp(ts / 1000): total_volume
            for ts, total_volume in coin_market_chart["total_volumes"]
        },
    }
