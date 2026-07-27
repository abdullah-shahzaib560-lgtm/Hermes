import pandas as pd
import httpx, time
import logging
import pycountry

from hermes.core.cache import RawCache

from datetime import timedelta

logger = logging.getLogger(__name__)

def iso3_to_iso2(iso3_code):
    try:
        return pycountry.countries.get(alpha_3=iso3_code.upper()).alpha_2
    except AttributeError:
        return "Not Found"

class IMF:

    def __init__(self, cache: RawCache | None = None):
        self._cache = cache or RawCache
        # FIX: The active production endpoint for modern SDMX data queries
        self.url: str = 'https://api.imf.org/external/sdmx/3.0/data/dataflow/'

    def _fetch(
        self,
        country: str,
        agency: str,
        dataflow_id: str,
        key: str,
        version: str = '~',
        timeout: float = 30.0,
        retries: int = 3
    ) -> pd.DataFrame:

        url = f'{self.url}{agency}/{dataflow_id}/{version}/{country}.{key}'
        headers = {"Accept": "application/json"}

        r = None
        for attempt in range(retries):
            try:
                resp = httpx.get(url=url, headers=headers, timeout=timeout, follow_redirects=True)
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

        data = r["data"]
        structure = data["structures"][0]

        series_dims = structure["dimensions"]["series"]
        obs_dim = structure["dimensions"]["observation"][0]
        time_values = [v["value"] for v in obs_dim["values"]]

        rows = []
        for series_key, series_obj in data["dataSets"][0]["series"].items():
            indices = [int(i) for i in series_key.split(":")]
            dim_values = {
                dim["id"]: dim["values"][idx]["id"]
                for dim, idx in zip(series_dims, indices)
            }
            for obs_idx, obs_val in series_obj["observations"].items():
                rows.append({
                    "date": time_values[int(obs_idx)],
                    "indicator_id": dim_values["INDICATOR"],
                    "country": dim_values["COUNTRY"],
                    "value": float(obs_val[0]),
                    "source": 'IMF',
                })

        data = pd.DataFrame(rows)

        data.set_index('date', inplace=True)
        data.sort_index(ascending=False, inplace=True)

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
        country: str,
        agency: str,
        dataflow_id: str,
        key: str,
        timeout: float = 30.0,
        retries: int = 3,
        force: bool = False
    ) -> pd.DataFrame:

        cache_params = {
            "country": country,
            "key": key,
            "agency": agency,
            "dataflow_id": dataflow_id,
        }

        return self._cache.get_or_fetch(
            source="world_bank",
            params=cache_params,
            fetch_fn=lambda: self._fetch(
                country, agency, dataflow_id,
                key, timeout, retries
            ),
            force=force,
            ttl=timedelta(days=7),  # WB data updates weekly
        )    