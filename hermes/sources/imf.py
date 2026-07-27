import pandas as pd
import httpx, time
import logging
from typing import Literal
import pycountry
from hermes.core.cache import RawCache

logger = logging.getLogger(__name__)

# For WEO series: https://imf.org.{country_iso2}.{series_id}.A
# For IFS series: https://imf.org.{country_iso2}.{series_id}.?

def iso3_to_iso2(iso3_code):
    try:
        return pycountry.countries.get(alpha_3=iso3_code.upper()).alpha_2
    except AttributeError:
        return "Not Found"

class IMF:

    def __init__(self, cache: RawCache | None = None):

        self._cache: RawCache = cache or RawCache
        self.url: str = 'https://imf.org'

    def _fetch(
        self,
        country_code: str,
        series_id: str,
        structure: str = Literal['WEO', 'IFS'],
        timeout: float = 30.0,
        retries: int = 3
    ) -> pd.DataFrame:


        iso2_c = iso3_to_iso2(country_code)

        if structure == 'WEO':
            url = f'{self.url}.{iso2_c}.{series_id}.A'
        if structure == 'IFS':
            url = f'{self.url}.{iso2_c}.{series_id}.?'

        for attempt in range(retries):
            try:
                resp = httpx.get(url=url, timeout=timeout)
                resp.raise_for_status()
                r = resp.json()
                break
            except httpx.ReadTimeout:
                if attempt == retries - 1:
                    raise
                time.sleep(2 ** attempt)
            except httpx.HTTPStatusError as e:
                logger.error(f'HTTP error: {e.response.status_code}')
                raise
        
        

