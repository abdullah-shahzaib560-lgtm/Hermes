import json
import logging
from datetime import timedelta
from typing import Optional

import pandas as pd
import urllib.request

from hermes.core.cache import RawCache

logger = logging.getLogger(__name__)

FAOSTAT_API = "https://fenixservices.fao.org/faostat/api/v1"


class FAO:
    def __init__(self, cache: RawCache | None = None):
        self._cache = cache

    def _fetch_json(self, url: str) -> dict | list:
        req = urllib.request.Request(url, headers={"User-Agent": "Hermes/0.1", "Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=60) as resp:
            return json.loads(resp.read().decode())

    def _cached(self, params: dict, fetch_fn, force: bool = False):
        if self._cache is None:
            return fetch_fn()
        return self._cache.get_or_fetch("fao", params, fetch_fn, force=force, ttl=timedelta(hours=24))

    def get_food_price_index(
        self,
        country: Optional[str] = None,
        year_from: Optional[int] = None,
        year_to: Optional[int] = None,
        normalize: bool = True,
        force: bool = False,
    ) -> pd.DataFrame:
        cache_params = {
            "q": "food_price_index", "country": country or "",
            "from": year_from or 0, "to": year_to or 0,
        }

        def _fetch():
            url = f"{FAOSTAT_API}/SDMX?domain=FP&indicator=FPI&area=5000&item=FPI"
            data = self._fetch_json(url)
            rows = []
            series = data if isinstance(data, list) else [data]
            for entry in series:
                if isinstance(entry, dict):
                    obs = entry.get("data", entry.get("observations", []))
                    for o in obs:
                        rows.append({
                            "date": o.get("time", o.get("period")),
                            "value": o.get("value", o.get("obsValue")),
                        })
            return pd.DataFrame(rows) if rows else pd.DataFrame()

        df = self._cached(cache_params, _fetch, force=force)
        if df.empty:
            return df
        return self._to_canonical(df) if normalize else df

    def get_aquastat(
        self,
        indicator: str = "water_stress",
        year: Optional[int] = None,
        normalize: bool = True,
        force: bool = False,
    ) -> pd.DataFrame:
        cache_params = {
            "q": "aquastat", "indicator": indicator, "year": year or 0,
        }

        def _fetch():
            url = f"{FAOSTAT_API}/SDMX?domain=AQ&indicator={indicator}"
            data = self._fetch_json(url)
            rows = []
            series = data if isinstance(data, list) else [data]
            for entry in series:
                if isinstance(entry, dict):
                    obs = entry.get("data", entry.get("observations", []))
                    for o in obs:
                        rows.append({
                            "country": o.get("area", o.get("country")),
                            "year": o.get("time", o.get("period")),
                            "value": o.get("value", o.get("obsValue")),
                            "indicator": indicator,
                        })
            return pd.DataFrame(rows) if rows else pd.DataFrame()

        df = self._cached(cache_params, _fetch, force=force)
        if df.empty:
            return df
        return self._to_indicator_canonical(df) if normalize else df

    def _to_canonical(self, df: pd.DataFrame) -> pd.DataFrame:
        if df.empty:
            return df
        out = pd.DataFrame()
        if "date" in df.columns:
            out["date"] = pd.to_datetime(df["date"].astype(str).str[:10], errors="coerce")
        elif "year" in df.columns:
            out["date"] = pd.to_datetime(df["year"].astype(str) + "-01-01", errors="coerce")
        out["country_iso3"] = "WLD"
        out["indicator_id"] = "FAO_FOOD_PRICE_INDEX"
        out["value"] = pd.to_numeric(df.get("value", pd.NA), errors="coerce")
        out["source"] = "FAO"
        for col in ["date", "country_iso3", "indicator_id", "value"]:
            if col not in out.columns:
                out[col] = None
        return out.dropna(subset=["value"]).reset_index(drop=True)

    def _to_indicator_canonical(self, df: pd.DataFrame) -> pd.DataFrame:
        if df.empty:
            return df
        out = pd.DataFrame()
        if "year" in df.columns:
            out["date"] = pd.to_datetime(df["year"].astype(str).str[:4] + "-01-01", errors="coerce")
        out["country_iso3"] = df.get("country", pd.NA).astype(str).str.upper().str[:3]
        out["indicator_id"] = df.get("indicator", "aquastat")
        out["value"] = pd.to_numeric(df.get("value", pd.NA), errors="coerce")
        out["source"] = "FAO"
        for col in ["date", "country_iso3", "indicator_id", "value"]:
            if col not in out.columns:
                out[col] = None
        return out.dropna(subset=["value"]).reset_index(drop=True)
