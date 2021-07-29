import datetime as dt
import logging
from collections import defaultdict
from typing import Dict, List, Optional, Union

import httpx

from app.client import coingecko_client, weisscrypto_client


def get_top_coins(n: int = 50) -> List[str]:
    response: httpx.Response = coingecko_client.get_search()
    all_coins = [x["id"] for x in response.json()["coins"]]
    return all_coins[:n]


def get_coin_prices(
    coin: str, days: Union[int, str, None] = None
) -> Dict[dt.date, float]:
    response: httpx.Response = coingecko_client.get_daily_market_chart(
        coin=coin, days=days
    )
    coin_data: Dict = response.json()
    return {
        dt.date.fromtimestamp(ts / 1000): price for ts, price in coin_data["prices"]
    }


def get_coin_market_caps(
    coin: str, days: Union[int, str, None] = None
) -> Dict[dt.date, float]:
    response: httpx.Response = coingecko_client.get_daily_market_chart(
        coin=coin, days=days
    )
    coin_data: Dict = response.json()
    return {
        dt.date.fromtimestamp(ts / 1000): market_cap
        for ts, market_cap in coin_data["market_caps"]
    }


def get_coin_total_volumes(
    coin: str, days: Union[int, str, None] = None
) -> Dict[dt.date, float]:
    response: httpx.Response = coingecko_client.get_daily_market_chart(
        coin=coin, days=days
    )
    coin_data: Dict = response.json()
    return {
        dt.date.fromtimestamp(ts / 1000): vol for ts, vol in coin_data["total_volumes"]
    }


def get_coins_prices(
    coins: List[str], days: Union[int, str, None] = None, min_days: Optional[int] = None
) -> Dict[dt.date, Dict[str, float]]:
    prices = defaultdict(dict)

    for coin in coins:
        coin_prices = get_coin_prices(coin, days)

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


def get_coins_market_caps(
    coins: List[str], days: Union[int, str, None] = None, min_days: Optional[int] = None
) -> Dict[dt.date, Dict[str, float]]:
    market_caps = defaultdict(dict)

    for coin in coins:
        coin_market_caps = get_coin_market_caps(coin, days)

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


def get_coins_total_volumes(
    coins: List[str], days: Union[int, str, None] = None, min_days: Optional[int] = None
) -> Dict[dt.date, Dict[str, float]]:
    total_volumes = defaultdict(dict)

    for coin in coins:
        coin_total_volumes = get_coin_total_volumes(coin, days)

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


def get_index_prices() -> Dict[dt.date, float]:
    response: httpx.Response = weisscrypto_client.get_w50_history()
    index_data: List = response.json()
    return {
        dt.datetime.fromisoformat(data[0][:-1]).date(): data[-1] for data in index_data
    }
