import pandas as pd
import logging, httpx, time
from datetime import timedelta

from hermes.core.cache import RawCache

logger = logging.getLogger(__name__)

class World_bank:

    def __init__(self, cache: RawCache | None = None):
        self.url = 'https://api.worldbank.org/v2'
        self._cache = cache or RawCache()

    def _fetch(
        self,
        country_code: str,
        indicator_code: str,
        frequency: str | None = None,
        most_recent: int | None = None,
        per_page: int = 1000,
        page: int = 1,
        timeout: float = 30.0,
        retries: int = 3,
    ) -> pd.DataFrame:

        url = f'{self.url}/country/{country_code}/indicator/{indicator_code}'
        params = {
            'per_page': per_page,
            'page': page,
            'format': 'json',
        }
        if frequency and most_recent:
            params['frequency'] = frequency
            params['mrv'] = most_recent

        r = None
        for attempt in range(retries):
            try:
                resp = httpx.get(url=url, params=params, timeout=timeout)
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
        if len(r) < 2 or not r[1]:
            logger.warning(f"No data: country={country_code}, indicator={indicator_code}")
            return pd.DataFrame(columns=[...])  # match whatever columns _fetch normally returns

        metadata, records = r[0], r[1]
        data = []

        for record in records:
            data.append({
                "date": record["date"],
                "indicator_id" : record["indicator"]["id"],
                "indicator_name": record['indicator']['value'],
                "country" : record['countryiso3code'],
                "value" : record['value'],
                "source" : "World_Bank"
            })

        data = pd.DataFrame(data)

        data.set_index('date', inplace=True)
        data.sort_index(ascending=False ,inplace=True)

        req = ['date','indicator_id','indicator_name','country','value','source']
        issues = 0
        for d in data:
            for r in req:
                if r not in d:
                    issues += 1

        logger.info(f'There is are total {issues} in the data')

        data = data.reset_index()
        return data
        

    def fetch(
        self,
        country_code: str,
        indicator_code: str,
        frequency: str | None = None,
        most_recent: int | None = None,
        per_page: int = 1000,
        page: int = 1,
        timeout: float = 30.0,
        retries: int = 3,
        force: bool = False
    ) -> pd.DataFrame:

        cache_params = {
            "country": country_code,
            "indicator": indicator_code,
            "frequency": frequency or "",
            "most_recent": most_recent or 0,
            "per_page": per_page,
        }

        return self._cache.get_or_fetch(
            source="world_bank",
            params=cache_params,
            fetch_fn=lambda: self._fetch(
                country_code, indicator_code, frequency,
                most_recent, per_page, page, timeout, retries
            ),
            force=force,
            ttl=timedelta(days=7),  # WB data updates weekly
        )    

if __name__ == '__main__':
    wb = World_bank()
    df = wb.fetch(
        country_code='USA',
        indicator_code='NY.GDP.MKTP.KD.ZG',
    )
    print(df)