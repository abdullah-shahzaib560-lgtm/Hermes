import pandas as pd
import logging
import pycountry

from hermes.core.cache import RawCache

logger = logging.getLogger(__name__)

def iso3_to_iso2(iso3_code):
    try:
        return pycountry.countries.get(alpha_3=iso3_code.upper()).alpha_2
    except AttributeError:
        return "Not Found"

class OpenSanction:

    def __init__(self, cache: RawCache):
        self._url = 'https://api.opensanctions.org'
        self._cache = RawCache() or cache

    def _fetch(
        self,
        country: str,
        dataset: str,
        topics: str = 'sanction'
    ) -> pd.DataFrame:

        ISO2 = iso3_to_iso2(iso3_code=country)
        
        url = f'{self._url}/search/{dataset}?countries={ISO2}&topics={topics}&limit=0'



