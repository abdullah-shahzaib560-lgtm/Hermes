import asyncio
import logging
from datetime import timedelta
from functools import partial
from typing import Literal

import aiohttp
import pandas as pd

from hermes.core.cache import RawCache

logger = logging.getLogger(__name__)

FinnhubEndpoint = Literal[
    "candles", 
    "quote",
    "profile",
    "metric",
    "peers",
    "earnings",
    "insider",
    "eps",
    "ebitda",
    "revenue",
    "news",
    "symbol",
]

class FINNHUB:

    BASE_URL = "https://finnhub.io/api/v1"

    ENDPOINTS = {
        "candles": "stock/candle",
        "quote": "quote",
        "profile": "stock/profile2",
        "metric": "stock/metric",
        "peers": "stock/peers",
        "earnings": "stock/earnings",
        "insider": "stock/insider-sentiment",
        "eps": "stock/eps-estimate",
        "ebitda": "stock/ebitda-estimate",
        "revenue": "stock/revenue-estimate",
        "news": "company-news",
        "symbol": "stock/symbol",
    }

    def __init__(
        self,
        api: str,
        cache: RawCache | None = None,
    ):
        self._api = api
        self._cache = cache or RawCache()
        self._url = self.BASE_URL

    def build_url(
        self,
        endpoint: FinnhubEndpoint,
    ) -> str:

        try:
            path = self.ENDPOINTS[endpoint]
        except KeyError:
            raise ValueError(
                f"Unsupported endpoint: {endpoint}"
            )

        return f"{self._url}/{path}"

    async def _fetch(
        self,
        endpoint: str,
        symbol: str,
        resolution: str,
        timeout: float = 30.0,
        retries: int = 3,
        _from: int | None = None,
        _to: int | None = None
    ) -> pd.DataFrame:

        params = {
            "token": self._api,
            "symbol": symbol
        }

        _url = self.build_url(endpoint=endpoint)

        if endpoint == 'candles':
            params['resolution'] = resolution
            params['from'] = _from
            params['to'] = _to
        elif endpoint == 'metric':
            params['metric'] = 'all'
        elif endpoint == 'insider':
            params['symbol'] = symbol
            params['from'] = _from
            params['to'] = _to
        elif endpoint == 'news':
            params['symbol'] = symbol
            params['from'] = _from
            params['to'] = _to

        r = None
        
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=timeout)) as client:
            for attempt in range(retries):
                try:
                    resp = await client.get(url=_url, params=params)
                    resp.raise_for_status()
                    r = await resp.json()
                    break
                except asyncio.TimeoutError:
                    if attempt == retries - 1:
                        raise
                    await asyncio.sleep(2**attempt)
                except aiohttp.ClientResponseError as e:
                    if e.status == 404:
                        logger.warning(f"404")
                        return r
                    logger.error(f"HTTP error: {e.status}")
                    raise