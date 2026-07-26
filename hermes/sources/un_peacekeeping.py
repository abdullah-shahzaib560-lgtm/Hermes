import logging
from datetime import timedelta
from pathlib import Path
from typing import Optional

import pandas as pd
import urllib.request

from hermes.core.cache import RawCache

logger = logging.getLogger(__name__)

UNPK_URL = "https://peacekeeping.un.org/sites/default/files/troop_contributors_2024.csv"


class UN_Peacekeeping:
    def __init__(self, cache: RawCache | None = None, data_dir: str | None = None):
        self._cache = cache
        self._data_dir = Path(data_dir) if data_dir else (Path.home() / ".hermes_cache" / "unpk")
        self._data_dir.mkdir(parents=True, exist_ok=True)

    def _download_csv(self) -> pd.DataFrame:
        csv_path = self._data_dir / "un_peacekeeping.csv"
        if csv_path.exists():
            age = pd.Timestamp.now() - pd.Timestamp.fromtimestamp(csv_path.stat().st_mtime)
            if age < timedelta(days=1):
                return pd.read_csv(csv_path)
        req = urllib.request.Request(UNPK_URL, headers={"User-Agent": "Hermes/0.1"})
        with urllib.request.urlopen(req, timeout=60) as resp:
            with open(csv_path, "wb") as f:
                f.write(resp.read())
        return pd.read_csv(csv_path)

    def _cached(self, params: dict, fetch_fn, force: bool = False):
        if self._cache is None:
            return fetch_fn()
        return self._cache.get_or_fetch("un_peacekeeping", params, fetch_fn, force=force, ttl=timedelta(hours=24))

    def get_data(
        self,
        country: Optional[str] = None,
        year: Optional[int] = None,
        normalize: bool = True,
        force: bool = False,
    ) -> pd.DataFrame:
        cache_params = {
            "q": "get_data", "country": country or "", "year": year or 0,
        }

        def _fetch():
            df = self._download_csv()
            df.columns = [str(c).strip().lower().replace(" ", "_") for c in df.columns]

            country_col = next((c for c in df.columns if "country" in c or "contributor" in c), None)
            troops_col = next((c for c in df.columns if "troop" in c or "total" in c or "personnel" in c), None)

            if not country_col:
                return pd.DataFrame()

            out = pd.DataFrame()
            out["country_iso3_raw"] = df[country_col].astype(str)
            out["year_val"] = year or 2024
            out["value"] = pd.to_numeric(df[troops_col], errors="coerce") if troops_col else 0
            out["indicator_id"] = "peacekeeping_troops"
            out = out.dropna(subset=["value"])

            if country:
                out = out[out["country_iso3_raw"].str.upper() == country.upper()]
            return out.reset_index(drop=True)

        df = self._cached(cache_params, _fetch, force=force)
        if df.empty:
            return df
        return self._to_canonical(df) if normalize else df

    def _to_canonical(self, df: pd.DataFrame) -> pd.DataFrame:
        if df.empty:
            return df
        out = pd.DataFrame()
        out["country_iso3"] = df["country_iso3_raw"].str.upper().str[:3]
        out["year"] = df["year_val"].astype(int)
        out["indicator_id"] = df["indicator_id"]
        out["value"] = df["value"]
        out["source"] = "UN Peacekeeping"
        return out.dropna(subset=["country_iso3", "indicator_id"]).reset_index(drop=True)
