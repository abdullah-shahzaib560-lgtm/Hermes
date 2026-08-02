import logging
import time
from datetime import timedelta

import httpx
import pandas as pd

from hermes.core.cache import RawCache

logger = logging.getLogger(__name__)


class IMF:
    def __init__(self, cache: RawCache | None = None):
        self._cache = cache or RawCache()
        self.url: str = "https://api.imf.org/external/sdmx/3.0/data/dataflow/"

    def _fetch(
        self,
        country: str,
        agency: str,
        dataflow_id: str,
        key: str,
        version: str = "~",
        timeout: float = 30.0,
        retries: int = 3,
    ) -> pd.DataFrame:

        url = f"{self.url}{agency}/{dataflow_id}/{version}/{country}.{key}"
        headers = {"Accept": "application/json"}

        empty = pd.DataFrame(columns=["date", "indicator_id", "country", "value", "source"])

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
                time.sleep(2**attempt)
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 404:
                    logger.warning(f"404: country={country}, dataflow={dataflow_id}, key={key}")
                    return empty
                logger.error(f"HTTP error: {e.response.status_code}")
                raise

        data = r["data"]
        structure = data["structures"][0]

        series_dims = structure["dimensions"]["series"]
        obs_dim = structure["dimensions"]["observation"][0]
        time_values = [v["value"] for v in obs_dim["values"]]

        dataset = data["dataSets"][0]
        if "series" not in dataset:
            logger.warning(f"No data: country={country}, dataflow={dataflow_id}, key={key}")
            return empty

        INDICATOR_DIM_CANDIDATES = ["INDICATOR", "INDEX_TYPE"]

        rows = []
        for series_key, series_obj in dataset["series"].items():
            indices = [int(i) for i in series_key.split(":")]
            dim_values = {dim["id"]: dim["values"][idx]["id"] for dim, idx in zip(series_dims, indices)}

            indicator_id = next(
                (dim_values[c] for c in INDICATOR_DIM_CANDIDATES if c in dim_values),
                key,
            )
            country_val = dim_values.get("COUNTRY", country)

            for obs_idx, obs_val in series_obj["observations"].items():
                raw_val = obs_val[0]
                if raw_val is None:
                    continue
                row = {
                    "date": time_values[int(obs_idx)],
                    "indicator_id": indicator_id,
                    "country": country_val,
                    "value": float(raw_val),
                    "source": "IMF",
                }

                for dim_id, dim_val in dim_values.items():
                    row.setdefault(dim_id, dim_val)
                rows.append(row)

        df = pd.DataFrame(rows)

        df.set_index("date", inplace=True)
        df.sort_index(ascending=False, inplace=True)

        req = ["indicator_id", "country", "value", "source"]
        missing = [c for c in req if c not in df.columns]
        if missing:
            logger.warning(f"Missing expected columns {missing} for {dataflow_id}/{key}")

        df = df.reset_index()
        return df

    def fetch(
        self,
        country: str,
        agency: str,
        dataflow_id: str,
        key: str,
        timeout: float = 30.0,
        retries: int = 3,
        force: bool = False,
    ) -> pd.DataFrame:

        cache_params = {
            "country": country,
            "key": key,
            "agency": agency,
            "dataflow_id": dataflow_id,
        }

        return self._cache.get_or_fetch(
            source="imf",
            params=cache_params,
            fetch_fn=lambda: self._fetch(
                country=country,
                agency=agency,
                dataflow_id=dataflow_id,
                key=key,
                timeout=timeout,
                retries=retries,
            ),
            force=force,
            ttl=timedelta(days=7),
        )
