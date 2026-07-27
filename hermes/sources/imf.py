import pandas as pd
import httpx, time
import logging
from typing import Literal
import pycountry
from hermes.core.cache import RawCache

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

        return pd.DataFrame(rows)



