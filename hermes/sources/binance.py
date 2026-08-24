import asyncio
import logging
import math
from datetime import UTC, datetime, timedelta
from functools import partial

import aiohttp
import pandas as pd

from hermes.constants import BINANCE_INTERVAL_MS
from hermes.core.cache import RawCache

logger = logging.getLogger(__name__)


class Binance:
    def __init__(self, cache: RawCache | None = None):
        self._spot_url = "https://api.binance.com"
        self._future_url = "https://fapi.binance.com"
        self._cache = cache or RawCache()

    _ENDPOINTS = {
        ("spot", "ohlcv"): ("api/v3/klines", ("interval", "limit")),
        ("spot", "trades"): ("api/v3/trades", ("limit",)),
        ("spot", "aggregated_trades"): ("api/v3/aggTrades", ("limit",)),
        ("spot", "order_book"): ("api/v3/depth", ("limit",)),
        ("spot", "best_bid_ask"): ("api/v3/ticker/bookTicker", ()),
        ("spot", "24hr"): ("api/v3/ticker/24hr", ()),
        ("spot", "exchangeInfo"): ("api/v3/exchangeInfo", ()),
        ("future", "ohlcv"): ("fapi/v1/klines", ("interval", "limit")),
        ("future", "trades"): ("fapi/v1/trades", ("limit",)),
        ("future", "aggregated_trades"): ("fapi/v1/aggTrades", ("limit",)),
        ("future", "order_book"): ("fapi/v1/depth", ("limit",)),
        ("future", "best_bid_ask"): ("fapi/v1/ticker/bookTicker", ()),
        ("future", "24hr"): ("fapi/v1/ticker/24hr", ()),
        ("future", "fundingRate"): ("fapi/v1/fundingRate", ("limit",)),
        ("future", "openInterest"): ("fapi/v1/openInterest", ()),
        ("future", "premiumIndex"): ("fapi/v1/premiumIndex", ()),
        ("future", "openInterestHist"): ("futures/data/openInterestHist", ("period", "limit")),
        ("future", "longShortRatio"): ("futures/data/globalLongShortAccountRatio", ("period", "limit")),
        ("future", "topLongShortAccountRatio"): ("futures/data/topLongShortAccountRatio", ("period", "limit")),
        ("future", "topLongShortPositionRatio"): ("futures/data/topLongShortPositionRatio", ("period", "limit")),
    }

    def _build_url(
        self,
        mode: str,
        endpoint: str,
        symbol: str,
        interval: str | None = None,
        limit: str | None = None,
        period: str | None = None,
        start_time: int | None = None,
        end_time: int | None = None,
    ):
        try:
            path, required = self._ENDPOINTS[(mode, endpoint)]
        except KeyError:
            raise ValueError(f"unknown endpoint {endpoint!r} for mode {mode!r}")

        base_url = self._spot_url if mode == "spot" else self._future_url
        params = {"symbol": symbol}

        provided = {"interval": interval, "limit": limit, "period": period}
        for name in required:
            if provided[name] is None:
                raise ValueError(f"{mode}/{endpoint} requires {name!r}")
            params[name] = provided[name]

        if start_time is not None:
            params["startTime"] = start_time
        if end_time is not None:
            params["endTime"] = end_time

        return f"{base_url.rstrip('/')}/{path}", params

    async def _fetch(
        self,
        mode: str,
        endpoint: str,
        symbol: str,
        interval: str | None = None,
        limit: int | None = None,
        period: str | None = None,
        start_time: int | None = None,
        end_time: int | None = None,
        retries: int = 3,
        timeout: float = 30.0,
    ):
        url, params = self._build_url(
            mode=mode,
            endpoint=endpoint,
            symbol=symbol,
            interval=interval,
            limit=limit,
            period=period,
            start_time=start_time,
            end_time=end_time,
        )

        r = None
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=timeout)) as client:
            for attempt in range(retries):
                try:
                    resp = await client.get(url=url, params=params)
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
                        logger.error("error 403")
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
        start_time: int | None = None,
        end_time: int | None = None,
        retries: int = 3,
        timeout: float = 30.0,
        force: bool = False,
    ):
        cached_params = {
            "symbol": symbol,
            "mode": mode,
            "endpoint": endpoint,
            "start_time": start_time,
            "end_time": end_time,
        }

        return await self._cache.get_or_fetch(
            source="binance",
            params=cached_params,
            fetch_fn=partial(
                self._fetch,
                endpoint=endpoint,
                symbol=symbol,
                interval=interval,
                limit=limit,
                period=period,
                mode=mode,
                start_time=start_time,
                end_time=end_time,
                timeout=timeout,
                retries=retries,
            ),
            force=force,
            ttl=timedelta(days=1),
        )

    async def fetch_history(
        self,
        symbol: str,
        interval: str = "1d",
        market: str = "future",
        years: int = 2,
        max_concurrent: int = 10,
    ) -> pd.DataFrame:
        interval_ms = BINANCE_INTERVAL_MS.get(interval)
        if interval_ms is None:
            raise ValueError(f"Unsupported interval: {interval!r}")

        now_ms = int(datetime.now(UTC).timestamp() * 1000)
        start_ms = now_ms - (years * 365 * 86_400_000)
        per_request_ms = 1000 * interval_ms

        num_requests = math.ceil((now_ms - start_ms) / per_request_ms)
        semaphore = asyncio.Semaphore(max_concurrent)

        async def _fetch_window(window_start: int, window_end: int) -> list:
            async with semaphore:
                data = await self.fetch(
                    mode=market,
                    endpoint="ohlcv",
                    symbol=symbol,
                    interval=interval,
                    limit=1000,
                    start_time=window_start,
                    end_time=window_end,
                    force=True,
                )
                return data if data else []

        tasks = []
        for i in range(num_requests):
            window_start = start_ms + (i * per_request_ms)
            window_end = min(window_start + per_request_ms, now_ms)
            tasks.append(_fetch_window(window_start, window_end))

        results = await asyncio.gather(*tasks, return_exceptions=True)

        all_candles = []
        for r in results:
            if isinstance(r, list):
                all_candles.extend(r)
            else:
                logger.warning(f"History fetch error: {r}")

        if not all_candles:
            return pd.DataFrame()

        df = pd.DataFrame(
            all_candles,
            columns=[
                "open_time",
                "open",
                "high",
                "low",
                "close",
                "volume",
                "close_time",
                "quote_volume",
                "trades_count",
                "taker_buy_volume",
                "taker_buy_quote_volume",
                "ignore",
            ],
        )

        for col in [
            "open",
            "high",
            "low",
            "close",
            "volume",
            "quote_volume",
            "taker_buy_volume",
            "taker_buy_quote_volume",
        ]:
            df[col] = df[col].astype(float)

        df["trades_count"] = df["trades_count"].astype(int)
        df = df.drop(columns=["ignore"])
        df = df.drop_duplicates(subset=["open_time"], keep="first")
        df = df.sort_values("open_time").reset_index(drop=True)

        return df
