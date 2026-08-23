import asyncio
import aiohttp
import logging
from functools import partial
from datetime import timedelta
from hermes.core.cache import RawCache

logger = logging.getLogger(__name__)

class Binance:

    def __init__(self, cache: RawCache | None = None):
        self._spot_url = 'https://api.binance.com'
        self._future_url = 'https://fapi.binance.com'
        self._cache = cache or RawCache()

    _ENDPOINTS = {
        ('spot', 'ohlcv'):              ('api/v3/klines',           ('interval', 'limit')),
        ('spot', 'trades'):             ('api/v3/trades',           ('limit',)),
        ('spot', 'aggregated_trades'):  ('api/v3/aggTrades',        ('limit',)),
        ('spot', 'order_book'):         ('api/v3/depth',            ('limit',)),
        ('spot', 'best_bid_ask'):       ('api/v3/ticker/bookTicker', ()),
        ('spot', '24hr'):               ('api/v3/ticker/24hr',      ()),
        ('spot', 'exchangeInfo'): ('api/v3/exchangeInfo', ()),

        ('future', 'ohlcv'):             ('fapi/v1/klines',           ('interval', 'limit')),
        ('future', 'trades'):            ('fapi/v1/trades',           ('limit',)),
        ('future', 'aggregated_trades'): ('fapi/v1/aggTrades',        ('limit',)),
        ('future', 'order_book'):        ('fapi/v1/depth',            ('limit',)),
        ('future', 'best_bid_ask'):      ('fapi/v1/ticker/bookTicker', ()),
        ('future', '24hr'):              ('fapi/v1/ticker/24hr',      ()),
        ('future', 'fundingRate'):       ('fapi/v1/fundingRate',      ('limit',)),
        ('future', 'openInterest'):      ('fapi/v1/openInterest',     ()),
        ('future', 'premiumIndex'):      ('fapi/v1/premiumIndex', ()),
        ('future', 'openInterestHist'):  ('futures/data/openInterestHist', ('period', 'limit')),
        ('future', 'longShortRatio'): ('futures/data/globalLongShortAccountRatio', ('period', 'limit')),
        ('future', 'topLongShortAccountRatio'): ('futures/data/topLongShortAccountRatio', ('period', 'limit')),
        ('future', 'topLongShortPositionRatio'): ('futures/data/topLongShortPositionRatio', ('period', 'limit')),
    }

    def _build_url(
        self,
        mode: str,
        endpoint: str,
        symbol: str,
        interval: str | None = None,
        limit: str | None = None,
        period: str | None = None,
    ):
        try:
            path, required = self._ENDPOINTS[(mode, endpoint)]
        except KeyError:
            raise ValueError(f'unknown endpoint {endpoint!r} for mode {mode!r}')

        base_url = self._spot_url if mode == 'spot' else self._future_url
        params = {'symbol': symbol}

        provided = {'interval': interval, 'limit': limit, 'period': period}
        for name in required:
            if provided[name] is None:
                raise ValueError(f'{mode}/{endpoint} requires {name!r}')
            params[name] = provided[name]

        return f'{base_url.rstrip("/")}/{path}', params

    async def _fetch(
        self,
        mode: str,
        endpoint: str,
        symbol: str,
        interval: str | None = None,
        limit: int | None = None,
        period: str | None = None,
        retries: int = 3,
        timeout: float = 30.0
    ):
        url, params = self._build_url(
            mode=mode,
            endpoint=endpoint,
            symbol=symbol,
            interval=interval,
            limit=limit,
            period=period
        )

        r = None
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=timeout)) as client:
            for attempt in range(retries):
                try:
                    resp = await client.get(url=url, params=params)
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
                    if e.status == 403:
                        logger.error('error 403')
                        continue
                    logger.error(f"HTTP error: {e.status}")
                    raise
        return r

    async def fetch(
        self,
        mode: str,
        endpoint: str,
        symbol: str,
        interval: str | None = None,
        limit: int | None = None,
        period: str | None = None,
        retries: int = 3,
        timeout: float = 30.0,
        force: bool = False
    ):
        cached_params = {
            'symbol': symbol,
            'mode': mode,
            'endpoint': endpoint
        }

        return await self._cache.get_or_fetch(
            source='finnhub',
            params=cached_params,
            fetch_fn=partial(
                self._fetch,
                endpoint=endpoint,
                symbol=symbol,
                interval=interval,
                limit=limit,
                period=period,
                mode=mode,
                timeout=timeout,
                retries=retries,
            ),
            force=force,
            ttl=timedelta(days=1)
        )

if __name__ == '__main__':
    async def main():
        binance = Binance()
        url, params = await binance._fetch(
            mode='spot',
            endpoint='ohlcv',
            symbol='BTCUSDT',
            interval='1m',
            limit=100
        )
        print(url, params)
    asyncio.run(main())