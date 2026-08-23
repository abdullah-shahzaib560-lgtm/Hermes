import asyncio
import logging
from datetime import timedelta
from functools import partial
from typing import Literal

import aiohttp

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
FinnhubEndpoints = [
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
        resolution: str | None = None,
        timeout: float = 30.0,
        retries: int = 3,
        _from: int | None = None,
        _to: int | None = None
    ):

        params = {
            "token": self._api,
            "symbol": symbol
        }

        _url = self.build_url(endpoint=endpoint)

        if endpoint == 'candles':
            if None in (resolution, _from, _to): raise ValueError('this endpoint requires resolution, _from and _to arguments')
            params['resolution'] = resolution
            params['from'] = _from
            params['to'] = _to
        elif endpoint == 'metric':
            params['metric'] = 'all'
        elif endpoint == 'insider':
            if None in (_from, _to): raise ValueError('this endpoint requires _from and _to arguments')
            params['from'] = _from
            params['to'] = _to
        elif endpoint == 'news':
            if None in (_from, _to): raise ValueError('this endpoint requires _from and _to arguments')
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
                except TimeoutError:
                    if attempt == retries - 1:
                        raise
                    await asyncio.sleep(2**attempt)
                except aiohttp.ClientResponseError as e:
                    if e.status == 404:
                        logger.warning("404")
                        return r
                    if e.status == 403:
                        logger.error('error 403')
                        continue
                    logger.error(f"HTTP error: {e.status}")
                    raise
        return r

    async def fetch(
        self,
        endpoint: str,
        symbol: str,
        resolution: str | None = None,
        _from: int | None = None,
        _to : int | None = None,
        timeout: float = 30.0,
        retries: int = 3,
        force: bool = False
    ):
        cached_params = {
            'endpoint': endpoint,
            'symbol': symbol,
            'resolution': resolution,
            '_to': _to,
            '_from': _from,
        }

        return await self._cache.get_or_fetch(
            source='finnhub',
            params=cached_params,
            fetch_fn=partial(
                self._fetch,
                endpoint=endpoint,
                symbol=symbol,
                resolution=resolution,
                _from=_from,
                _to=_to,
                timeout=timeout,
                retries=retries,
            ),
            force=force,
            ttl=timedelta(days=7)
        )



if __name__ == "__main__":
    async def main():
        fin = FINNHUB(api="da45rr9r01qo2j8743egda45rr9r01qo2j8743f0")

        async def finn_eps_estimate(symbol: str):
            return await fin.fetch(endpoint='eps', symbol=symbol)

        async def finn_revenue_estimate(symbol: str):
            return await fin.fetch(endpoint='revenue', symbol=symbol)

        async def finn_ebitda_estimate(symbol: str):
            return await fin.fetch(endpoint='ebitda', symbol=symbol)

        print(await finn_ebitda_estimate('AAPL'))
        print(await finn_eps_estimate('AAPL'))
        print(await finn_revenue_estimate('AAPL'))

    asyncio.run(main())
