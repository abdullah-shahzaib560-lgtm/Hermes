import pandas as pd
from aiohttp import ClientSession, ClientTimeout, ClientResponseError 
import aiohttp 
import logging
import asyncio

from hermes.core.cache import RawCache
from hermes.sources.lib._alphavantage import FREE_ALPHA_VANTAGE_FUNCTIONS
logger = logging.getLogger(__name__)

class AlphaVintage:

    def __init__(self, api: str, cache: RawCache | None = None):
        # self._cache = cache or RawCache()
        self._api = api
        self._url = 'https://www.alphavantage.co/query'

    def free_fns(self):
        return FREE_ALPHA_VANTAGE_FUNCTIONS
    
    async def _fetch(
        self,
        fn: str,
        symbol: str,
        timeout: float = 30.0,
        retries: int = 3
    ) -> pd.DataFrame:
        
        params = {
            "function": fn,
            "symbol": symbol,
            "apikey": self._api,          
            "outputsize": "compact",      
            "datatype": "json"
            }

        r = None
        
        timeout_obj = ClientTimeout(total=timeout)

        async with ClientSession(timeout=timeout_obj) as client:
            for attempt in range(retries):
                try:
                    resp = await client.get(url=self._url, params=params)
                    resp.raise_for_status()
                    r = await resp.content.decode()  
                    break
                except asyncio.TimeoutError: 
                    if attempt == retries - 1:
                        raise
                    await asyncio.sleep(2**attempt)
                except ClientResponseError as e:
                    if e.status == 404: 
                        logger.warning(f"404")
                        return r
                    logger.error(f"HTTP error: {e.status}")
                    raise

        return r

if __name__ == '__main__':

    async def main():
        alpha = AlphaVintage(api='3BDTWLX34ZO0XGI1')
        data = await alpha._fetch(
            fn='TIME_SERIES_DAILY',
            symbol='AAPL'
        )
        print(data)

    asyncio.run(main())
