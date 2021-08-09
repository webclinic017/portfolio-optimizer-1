import datetime as dt
import logging
from collections import defaultdict
from typing import Dict, List, Optional, Union

from client import coingecko_client


async def get_top_coins(n: int = 50) -> List[str]:
    return await coingecko_client.get_top_coins(vs_currency="usd", per_page=n)


async def get_coin_prices(
    coin: str, days: Union[int, str, None] = None
) -> Dict[dt.date, float]:
    coin_data: Dict = await coingecko_client.get_coin_market_chart(
        coin_id=coin, vs_currency="usd", days=days
    )
    return coin_data["prices"]


async def get_coin_market_caps(
    coin: str, days: Union[int, str, None] = None
) -> Dict[dt.date, float]:
    coin_data: Dict = await coingecko_client.get_coin_market_chart(
        coin_id=coin, vs_currency="usd", days=days
    )
    return coin_data["market_caps"]


async def get_coin_total_volumes(
    coin: str, days: Union[int, str, None] = None
) -> Dict[dt.date, float]:
    coin_data: Dict = await coingecko_client.get_coin_market_chart(
        coin_id=coin, vs_currency="usd", days=days
    )
    return coin_data["total_volumes"]


async def get_coins_prices(
    coins: List[str], days: Union[int, str, None] = None, min_days: Optional[int] = None
) -> Dict[dt.date, Dict[str, float]]:
    prices = defaultdict(dict)

    for coin in coins:
        coin_prices = await get_coin_prices(coin, days)

        if min_days is not None and len(coin_prices) < min_days:
            logging.getLogger().warning(
                "Discarding prices for %s with length %d which is less than %d.",
                coin,
                len(coin_prices),
                min_days,
            )
            continue

        for date in coin_prices:
            prices[date][coin] = coin_prices[date]

    return dict(prices)


async def get_coins_market_caps(
    coins: List[str], days: Union[int, str, None] = None, min_days: Optional[int] = None
) -> Dict[dt.date, Dict[str, float]]:
    market_caps = defaultdict(dict)

    for coin in coins:
        coin_market_caps = await get_coin_market_caps(coin, days)

        if min_days is not None and len(coin_market_caps) < min_days:
            logging.getLogger().warning(
                "Discarding market caps for %s with length %d which is less than %d.",
                coin,
                len(coin_market_caps),
                min_days,
            )
            continue

        for date in coin_market_caps:
            market_caps[date][coin] = coin_market_caps[date]

    return dict(market_caps)


async def get_coins_total_volumes(
    coins: List[str], days: Union[int, str, None] = None, min_days: Optional[int] = None
) -> Dict[dt.date, Dict[str, float]]:
    total_volumes = defaultdict(dict)

    for coin in coins:
        coin_total_volumes = await get_coin_total_volumes(coin, days)

        if min_days is not None and len(coin_total_volumes) < min_days:
            logging.getLogger().warning(
                "Discarding total volumes for %s with length %d which is less than %d.",
                coin,
                len(coin_total_volumes),
                min_days,
            )
            continue

        for date in coin_total_volumes:
            total_volumes[date][coin] = coin_total_volumes[date]

    return dict(total_volumes)
