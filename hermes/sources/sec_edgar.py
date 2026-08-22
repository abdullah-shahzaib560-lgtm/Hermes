import asyncio
import logging
from typing import Literal, Dict

from datetime import timedelta
from functools import partial

import aiohttp
import pandas as pd

from hermes.core.helper import get_CIK
from hermes.core.cache import RawCache
logger = logging.getLogger(__name__)


class SECEDGAR:

    def __init__(self, username: str, email: str, cache: RawCache | None = None):
        self._email = email
        self._username = username
        self._cache = cache or RawCache()
        self._url = "https://data.sec.gov/api/xbrl/companyfacts"

    async def _fetch(self, symbol: str, retries: int = 3, timeout: float = 30.0):
        cik = get_CIK(ticker=symbol)
        print(cik)
        url = f'{self._url}/{cik}.json'

        headers = {
            "User-Agent": f"{self._username} {self._email}"
        }

        r = None
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=timeout)) as client:
            for attempt in range(retries):
                try:
                    resp = await client.get(url=url, headers=headers)
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

        return r

    async def fetch(
        self,
        company: str,
        mode: Literal["full", "imp"] = "imp",
        timeout: float = 30.0,
        retries: int = 3,
        force: bool = False,
    ) -> pd.DataFrame | Dict:

        cache_params = {
            "company": company,
            "mode": mode,
        }

        return await self._cache.get_or_fetch(
            source="sec_edgar",
            params=cache_params,
            fetch_fn=partial(
                self._fetch,
                company=company,
                mode=mode,
                timeout=timeout,
                retries=retries,
            ),
            force=force,
            ttl=timedelta(days=7),
        )
    
if __name__ == "__main__":

    async def main():

        sec = SECEDGAR(
            email="ha%ra%li.de%v9#^^m",
            username="S3e@l"
        )

        df = await sec._fetch(
            symbol="AAPL"
        )
        import json
        with open("data.json", "w") as json_file:
            json.dump(df, json_file, indent=4)

    asyncio.run(main())