import datetime as dt
from typing import Dict, List, Union

import httpx
from client import coingecko_client, weisscrypto_client


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


def get_index_prices():
    response: httpx.Response = weisscrypto_client.get_w50_history()
    index_data: List = response.json()
    return {
        dt.datetime.fromisoformat(data[0][:-1]).date(): data[-1] for data in index_data
    }
