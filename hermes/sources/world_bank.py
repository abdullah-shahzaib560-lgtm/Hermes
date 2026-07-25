import pandas as pd
import logging
import json
import urllib.request
import urllib.error
from typing import Optional

from hermes.core.cache import RawCache

logger = logging.getLogger(__name__)

BASE_URL = "https://api.worldbank.org/v2"


class World_Bank:
    def __init__(self, cache: RawCache | None = None):
        self._cache = cache

    def _fetch_json(self, url: str) -> list | dict:
        req = urllib.request.Request(url, headers={"User-Agent": "Hermes/0.1"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode())

    def _cached(self, params: dict, fetch_fn, force: bool = False):
        if self._cache is None:
            return fetch_fn()
        return self._cache.get_or_fetch("world_bank", params, fetch_fn, force=force)

    def get_data(
        self,
        indicator: str,
        country: str = "all",
        date: Optional[str] = None,
        per_page: int = 1000,
        normalize: bool = True,
        force: bool = False,
    ) -> pd.DataFrame:
        cache_params = {
            "q": "get_data",
            "indicator": indicator,
            "country": country,
            "date": date or "",
        }

        def _fetch():
            records = []
            page = 1
            while True:
                params = {"format": "json", "per_page": min(per_page, 1000), "page": page}
                if date:
                    params["date"] = date
                qs = "&".join(f"{k}={v}" for k, v in params.items())
                url = f"{BASE_URL}/country/{country}/indicator/{indicator}?{qs}"
                data = self._fetch_json(url)
                if not data or len(data) < 2 or not data[1]:
                    break
                records.extend(data[1])
                total = data[0].get("pages", 1)
                if page >= total:
                    break
                page += 1
            return pd.DataFrame(records)

        df = self._cached(cache_params, _fetch, force=force)
        if df.empty:
            return df
        return self._to_canonical(df) if normalize else df

    def search_indicators(self, query: str, per_page: int = 100) -> pd.DataFrame:
        qs = f"format=json&search={urllib.parse.quote(query)}&per_page={per_page}"
        url = f"{BASE_URL}/indicator?{qs}"
        data = self._fetch_json(url)
        if not data or len(data) < 2:
            return pd.DataFrame()
        rows = []
        for item in data[1]:
            rows.append({"indicator_id": item.get("id"), "name": item.get("name")})
        return pd.DataFrame(rows)

    def _to_canonical(self, df: pd.DataFrame) -> pd.DataFrame:
        out = pd.DataFrame()
        dates = df.get("date", pd.NA)
        if not dates.isna().all():
            out["date"] = pd.to_datetime(dates, format="%Y", errors="coerce")

        iso3 = df.get("countryiso3code", pd.NA)
        if not iso3.isna().all():
            out["country_iso3"] = iso3.astype(str).str.upper()

        indicator_raw = df.get("indicator", pd.NA)
        if not indicator_raw.isna().all():
            out["indicator_id"] = indicator_raw.apply(
                lambda x: x.get("id") if isinstance(x, dict) else None
            )

        values = pd.to_numeric(df.get("value", pd.NA), errors="coerce")
        if not values.isna().all():
            out["value"] = values

        out["source"] = "World Bank"
        return out.dropna(subset=["date", "country_iso3", "indicator_id"])
