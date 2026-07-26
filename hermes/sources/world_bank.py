import json
import logging
from datetime import timedelta
import urllib.error
import urllib.parse
import urllib.request
from typing import Optional

import pandas as pd

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
        return self._cache.get_or_fetch("world_bank", params, fetch_fn, force=force, ttl=timedelta(hours=24))

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
                total_pages = data[0].get("pages", 1)
                if page >= total_pages:
                    break
                page += 1
            return pd.DataFrame(records) if records else pd.DataFrame()

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
        if df.empty:
            return df
        out = pd.DataFrame()
        date_raw = df.get("date")
        if date_raw is not None:
            out["date"] = pd.to_datetime(date_raw, format="%Y", errors="coerce")

        iso3 = df.get("countryiso3code")
        if iso3 is not None:
            out["country_iso3"] = iso3.astype(str).str.upper().str.strip()

        indicator_raw = df.get("indicator")
        if indicator_raw is not None:
            out["indicator_id"] = indicator_raw.apply(
                lambda x: x.get("id") if isinstance(x, dict) else None
            )

        value_raw = df.get("value")
        if value_raw is not None:
            out["value"] = pd.to_numeric(value_raw, errors="coerce")

        out["source"] = "World Bank"
        needed = ["date", "country_iso3", "indicator_id", "value"]
        for col in needed:
            if col not in out.columns:
                out[col] = None
        return out.dropna(subset=["date", "country_iso3", "indicator_id"]).reset_index(drop=True)
