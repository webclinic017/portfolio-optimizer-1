from typing import Dict, List

import pandas as pd
import requests_cache
import yfinance as yf

SHARED_SESSION = requests_cache.CachedSession(
    "yfinance_http_cache", backend="memory", expire_after=60 * 60
)


def download(
    tickers: List[str], period: str = "max", interval: str = "1d"
) -> pd.DataFrame:
    dfs: Dict = {}

    for t in (t.upper() for t in tickers):
        dfs[t] = yf.Ticker(t, SHARED_SESSION).history(
            period=period,
            interval=interval,
            start=None,
            end=None,
            auto_adjust=False,
            back_adjust=False,
            actions=False,
            prepost=False,
            proxy=None,
            rounding=False,
            many=True,
        )

    return pd.concat(dfs.values(), axis=1, keys=dfs.keys())
