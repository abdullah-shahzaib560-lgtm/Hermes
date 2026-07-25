import pandas as pd
import logging
import xml.etree.ElementTree as ET
import urllib.request
import urllib.parse
import json
from typing import Optional
from io import StringIO

from hermes.core.cache import RawCache

logger = logging.getLogger(__name__)

SDMX_BASE = "http://dataservices.imf.org/REST/SDMX_XML.svc"


class IMF:
    DATABASES = {"IFS": "IFS", "WEO": "WEO", "GFS": "GFS", "BOP": "BOP"}

    def __init__(self, cache: RawCache | None = None):
        self._cache = cache

    def _fetch_text(self, url: str) -> str:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=60) as resp:
            return resp.read().decode()

    def _fetch_csv(self, url: str) -> str:
        req = urllib.request.Request(url, headers={"Accept": "text/csv"})
        with urllib.request.urlopen(req, timeout=60) as resp:
            return resp.read().decode()

    def _cached(self, params: dict, fetch_fn, force: bool = False):
        if self._cache is None:
            return fetch_fn()
        return self._cache.get_or_fetch("imf", params, fetch_fn, force=force)

    def get_data(
        self,
        database: str = "IFS",
        indicator: Optional[str] = None,
        country: str = "all",
        freq: str = "A",
        start_period: Optional[str] = None,
        end_period: Optional[str] = None,
        normalize: bool = True,
        force: bool = False,
    ) -> pd.DataFrame:
        db = self.DATABASES.get(database.upper(), database.upper())
        cache_params = {
            "q": "get_data", "db": db, "indicator": indicator or "",
            "country": country, "freq": freq,
            "start": start_period or "", "end": end_period or "",
        }

        def _fetch():
            key = f"{freq}.{country}"
            if indicator:
                key = f"{freq}.{country}.{indicator}"
            params = {}
            if start_period:
                params["startPeriod"] = start_period
            if end_period:
                params["endPeriod"] = end_period
            qs = "&".join(f"{k}={v}" for k, v in params.items()) if params else ""
            url = f"{SDMX_BASE}/CompactData/{db}/{key}?{qs}" if qs else f"{SDMX_BASE}/CompactData/{db}/{key}"
            raw = self._fetch_csv(url)
            return pd.read_csv(StringIO(raw))

        df = self._cached(cache_params, _fetch, force=force)
        if df.empty:
            return df
        return self._to_canonical(df, database) if normalize else df

    def _to_canonical(self, df: pd.DataFrame, database: str) -> pd.DataFrame:
        out = pd.DataFrame()
        time_cols = [c for c in df.columns if c.startswith("TIME_PERIOD") or c in ("TimePeriod", "time", "year")]
        if time_cols:
            out["date"] = pd.to_datetime(df[time_cols[0]].astype(str).str[:10], errors="coerce")

        area_cols = [c for c in df.columns if c in ("REF_AREA", "ReferenceArea", "country", "Country")]
        for c in area_cols:
            if c in df.columns and not df[c].isna().all():
                out["country_iso3"] = df[c].astype(str).str.upper().str[:3]
                break

        ind_cols = [c for c in df.columns if c in ("INDICATOR", "Indicator", "indicator")]
        for c in ind_cols:
            if c in df.columns and not df[c].isna().all():
                out["indicator_id"] = df[c].astype(str)
                break

        val_cols = [c for c in df.columns if c in ("OBS_VALUE", "ObsValue", "value", "Value")]
        for c in val_cols:
            if c in df.columns:
                out["value"] = pd.to_numeric(df[c], errors="coerce")
                break

        out["source"] = f"IMF {database}"
        return out.dropna(subset=["date", "value"])
