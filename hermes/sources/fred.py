import asyncio
import logging
from datetime import timedelta
from functools import partial

import aiohttp
import pandas as pd

from hermes.core.cache import RawCache

logger = logging.getLogger(__name__)

fred_series = [
    # Growth
    "GDPC1",  # Real GDP
    "A191RL1Q225SBEA",  # GDP growth
    "INDPRO",  # Industrial Production
    # Inflation
    "CPIAUCSL",  # CPI
    "CPILFESL",  # Core CPI
    "PCEPI",  # PCE
    "PCEPILFE",  # Core PCE
    # Employment
    "UNRATE",  # Unemployment
    "PAYEMS",  # Nonfarm Payrolls
    "CIVPART",  # Labor Force Participation
    # Interest rates
    "FEDFUNDS",  # Fed Funds Rate
    "DGS10",  # 10Y Treasury
    "DGS2",  # 2Y Treasury
    "DGS3MO",  # 3M Treasury
    # Yield curve
    "T10Y2Y",  # 10Y - 2Y
    "T10Y3M",  # 10Y - 3M
    # Money/credit
    "M2SL",  # M2
    "TOTBKCR",  # Bank Credit
    # Housing
    "HOUST",  # Housing Starts
    "EXHOSLUSM495S",  # Existing Home Sales
    # Markets
    "SP500",  # S&P 500
    "VIXCLS",  # VIX
    # Dollar
    "DTWEXBGS",  # USD Index
]

# https://api.stlouisfed.org/fred/series/observations?series_id=GNPCA&api_key={api}&file_type=json


class FRED:
    def __init__(self, api: str, cache: RawCache | None = None):
        self._cache = cache or RawCache()
        self._url = "https://api.stlouisfed.org/fred/series/observations"
        self._api = api

    async def _fetch(self, series_id: str, timeout: float = 30.0, retries: int = 3) -> pd.DataFrame:

        params = {"series_id": series_id, "api_key": self._api, "file_type": "json"}

        r = None
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=timeout)) as client:
            for attempt in range(retries):
                try:
                    resp = await client.get(url=self._url, params=params)
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
                    logger.error(f"HTTP error: {e.status}")
                    raise

        df = pd.DataFrame(r["observations"])
        df.drop(columns=["realtime_start", "realtime_end"], inplace=True)
        df["series_id"] = series_id
        df["unit"] = r["units"]
        df = df.set_index("date")
        df = df.sort_index(ascending=False)
        return df

    async def fetch(self, series_id: str, timeout: float = 30.0, retries: int = 3, force: bool = False) -> pd.DataFrame:

        cached_params = {"series_id": series_id}

        return await self._cache.get_or_fetch(
            source="fred",
            params=cached_params,
            fetch_fn=partial(
                self._fetch,
                series_id=series_id,
                timeout=timeout,
                retries=retries,
            ),
            force=force,
            ttl=timedelta(days=30),
        )


