import datetime as dt
from typing import Dict, Optional

import httpx
import pytz

from app.client import av_client

DATE_FORMAT = "%Y-%m-%d"


def get_stock_prices(symbol: str, days: Optional[int] = None) -> Dict:
    response: httpx.Response = av_client.get_daily_market_chart(symbol=symbol)
    full_data = response.json()
    metadata = full_data["Meta Data"]
    tz = pytz.timezone(metadata["5. Time Zone"])
    daily_prices = full_data["Time Series (Daily)"]

    result = {}
    today = dt.datetime.now().astimezone(tz).date()

    for d in daily_prices:
        date = dt.datetime.strptime(d, DATE_FORMAT).replace(tzinfo=tz).date()

        if days and date + dt.timedelta(days=days) < today:
            break

        result[date] = daily_prices[d]["4. close"]

    return result


if __name__ == "__main__":
    print(get_stock_prices("AAPL", days=5))
