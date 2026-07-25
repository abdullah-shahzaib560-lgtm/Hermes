import pandas as pd
import logging
import httpx
import xml.etree.ElementTree as ET
from typing import Optional
from io import StringIO

from hermes.core.cache import RawCache

logger = logging.getLogger(__name__)

SDMX_BASE = "https://sdmx.imf.org/datastore/data"


class IMF:
    DATABASES = {
        "IFS": "IFS",
        "WEO": "WEO",
        "GFS": "GFS",
        "BOP": "BOP",
    }

    def __init__(self, cache: RawCache | None = None):
        self.base_url = SDMX_BASE
        self._cache = cache

    def _cached(self, params: dict, fetch_fn, force: bool = False):
        if self._cache is None:
            return fetch_fn()
        return self._cache.get_or_fetch("imf", params, fetch_fn, force=force)

    def get_data(
        self,
        database: str = "IFS",
        indicator: Optional[str] = None,
        country: str = "all",
        start_period: Optional[str] = None,
        end_period: Optional[str] = None,
        normalize: bool = True,
        force: bool = False,
    ) -> pd.DataFrame:
        cache_params = {
            "action": "get_data",
            "database": database,
            "indicator": indicator or "",
            "country": country,
            "start_period": start_period or "",
            "end_period": end_period or "",
        }

        def _fetch():
            db = self.DATABASES.get(database.upper(), database)
            freq = "A"

            if indicator:
                key = f"{freq}.{country}.{indicator}"
            else:
                key = f"{freq}.{country}"

            params = {}
            if start_period:
                params["startPeriod"] = start_period
            if end_period:
                params["endPeriod"] = end_period

            url = f"{self.base_url}/{db}/{key}"
            resp = httpx.get(url, params=params, timeout=60, headers={
                "Accept": "application/vnd.sdmx.data+csv; charset=utf-8"
            })
            resp.raise_for_status()
            return pd.read_csv(StringIO(resp.text))

        df = self._cached(cache_params, _fetch, force=force)
        if df.empty:
            return df
        return self._to_canonical(df, database) if normalize else df

    def search_indicators(self, query: str, database: str = "IFS") -> pd.DataFrame:
        db = self.DATABASES.get(database.upper(), database)
        url = f"{SDMX_BASE}/{db}"
        resp = httpx.get(url, timeout=30)
        resp.raise_for_status()
        root = ET.fromstring(resp.content)
        ns = {"message": "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message",
              "structure": "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure"}
        items = []
        for c in root.iter():
            items.append({"indicator": "unavailable via SDMX search"})
        return pd.DataFrame(items)

    def _to_canonical(self, df: pd.DataFrame, database: str) -> pd.DataFrame:
        out = pd.DataFrame()
        date_cols = [c for c in df.columns if c.startswith("TIME_PERIOD")]
        if date_cols:
            out["date"] = pd.to_datetime(df[date_cols[0]], errors="coerce")
        elif "TIME_PERIOD" in df.columns:
            out["date"] = pd.to_datetime(df["TIME_PERIOD"], errors="coerce")

        ref_area = df.get("REF_AREA", df.get("REFERENCE_AREA", pd.NA))
        if not ref_area.isna().all():
            out["country_iso3"] = ref_area

        indicator_col = df.get("INDICATOR", df.get("INDICATOR_ID", pd.NA))
        if not indicator_col.isna().all():
            out["indicator_id"] = indicator_col

        if "OBS_VALUE" in df.columns:
            out["value"] = pd.to_numeric(df["OBS_VALUE"], errors="coerce")
        elif "VALUE" in df.columns:
            out["value"] = pd.to_numeric(df["VALUE"], errors="coerce")

        out["source"] = f"IMF {database}"
        return out.dropna(subset=["date", "value"])
