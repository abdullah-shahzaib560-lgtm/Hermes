import asyncio
import logging
from datetime import timedelta
from functools import partial
from typing import Literal

import pandas as pd
import yfinance as yf

from hermes.core.cache import RawCache

logger = logging.getLogger(__name__)

YfinanceEndpoint = Literal[
    "eps_estimate",
    "revenue_estimate",
    "earnings_history",
]

YfinanceEndpoints = [
    "eps_estimate",
    "revenue_estimate",
    "earnings_history",
]


class Yfinance:

    def __init__(
        self,
        cache: RawCache | None = None,
    ):
        self._cache = cache or RawCache()

    async def _fetch(
        self,
        endpoint: YfinanceEndpoint,
        symbol: str,
    ):

        ticker = yf.Ticker(symbol)

        if endpoint == "quote":
            return ticker.info
        elif endpoint == "eps_estimate":
            df = ticker.earnings_estimate
            return df.to_dict() if df is not None and not df.empty else None
        elif endpoint == "revenue_estimate":
            df = ticker.revenue_estimate
            return df.to_dict() if df is not None and not df.empty else None
        elif endpoint == "earnings_history":
            df = ticker.earnings_history
            return df.to_dict() if df is not None and not df.empty else None
        else:
            raise ValueError(f"Unsupported endpoint: {endpoint}")

    async def fetch(
        self,
        endpoint: YfinanceEndpoint,
        symbol: str,
        force: bool = False,
    ):
        cached_params = {
            "endpoint": endpoint,
            "symbol": symbol,
        }

        return await self._cache.get_or_fetch(
            source="yfinance",
            params=cached_params,
            fetch_fn=partial(
                self._fetch,
                endpoint=endpoint,
                symbol=symbol,
            ),
            force=force,
            ttl=timedelta(days=1),
        )


if __name__ == "__main__":
    import asyncio
    import json

    import pandas as pd

    # Custom function to safely turn Pandas objects into clean text/numbers
    def clean_json(obj):
        if isinstance(obj, dict):
            return {str(k): clean_json(v) for k, v in obj.items()}
        if isinstance(obj, list):
            return [clean_json(i) for i in obj]
        if isinstance(obj, pd.Timestamp) or hasattr(obj, "isoformat"):
            return obj.isoformat()
        if pd.isna(obj):  # Handles NaN, NaT, and None safely
            return None
        return obj

    async def main():
        yf_source = Yfinance()

        for endpoint in YfinanceEndpoints:
            data = await yf_source.fetch(endpoint=endpoint, symbol='AAPL')

            # Use .name or .value to get a clean string for the filename
            filename = f"{endpoint}.json"

            with open(filename, "w") as json_file:
                # Clean the entire data structure before saving
                serializable_data = clean_json(data)
                json.dump(serializable_data, json_file, indent=4)

    asyncio.run(main())
