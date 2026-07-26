import logging
from datetime import timedelta
from pathlib import Path
from typing import Optional

import pandas as pd
import urllib.request

from hermes.core.cache import RawCache

logger = logging.getLogger(__name__)

COW_ALLIANCE_URL = "https://correlatesofwar.org/wp-content/uploads/version4.1_csv.zip"


class COW:
    def __init__(self, cache: RawCache | None = None, data_dir: str | None = None):
        self._cache = cache
        self._data_dir = Path(data_dir) if data_dir else (Path.home() / ".hermes_cache" / "cow")
        self._data_dir.mkdir(parents=True, exist_ok=True)

    def _download_csv(self) -> pd.DataFrame:
        csv_path = self._data_dir / "cow_alliances.csv"
        if csv_path.exists():
            age = pd.Timestamp.now() - pd.Timestamp.fromtimestamp(csv_path.stat().st_mtime)
            if age < timedelta(days=30):
                return pd.read_csv(csv_path)
        req = urllib.request.Request(COW_ALLIANCE_URL, headers={"User-Agent": "Hermes/0.1"})
        with urllib.request.urlopen(req, timeout=120) as resp:
            with open(csv_path, "wb") as f:
                f.write(resp.read())
        return pd.read_csv(csv_path)

    def _cached(self, params: dict, fetch_fn, force: bool = False):
        if self._cache is None:
            return fetch_fn()
        return self._cache.get_or_fetch("cow", params, fetch_fn, force=force, ttl=timedelta(days=30))

    def get_data(
        self,
        country: Optional[str] = None,
        year_from: Optional[int] = None,
        year_to: Optional[int] = None,
        alliance_type: Optional[int] = None,
        normalize: bool = True,
        force: bool = False,
    ) -> pd.DataFrame:
        cache_params = {
            "q": "get_data", "country": country or "",
            "from": year_from or 0, "to": year_to or 0,
            "type": alliance_type or 0,
        }

        def _fetch():
            df = self._download_csv()
            df.columns = [str(c).strip() for c in df.columns]
            state_col = next((c for c in df.columns if "state" in c.lower() and "name" in c.lower()), None)
            state_abbr = next((c for c in df.columns if "state" in c.lower() and "abbr" in c.lower()), None)
            year_col = next((c for c in df.columns if c.lower() in ("year", "start_year", "styear", "st_yr")), None)
            end_col = next((c for c in df.columns if c.lower() in ("end_year", "endyear", "en_yr")), None)
            type_col = next((c for c in df.columns if c.lower() in ("type", "alliance_type", "defense")), None)

            if not (state_abbr and year_col):
                return pd.DataFrame()

            out = pd.DataFrame()
            out["country_code"] = df[state_abbr].astype(str).str.upper().str[:3]
            out["year_val"] = pd.to_numeric(df[year_col], errors="coerce")

            if end_col:
                out["year_end"] = pd.to_numeric(df[end_col], errors="coerce")
            else:
                out["year_end"] = 2026

            if type_col:
                out["alliance_type"] = pd.to_numeric(df[type_col], errors="coerce")
                out["severity"] = out["alliance_type"].map({
                    1: 1.0, 2: 0.7, 3: 0.5, 4: 0.3,
                }).fillna(0.5)
            else:
                out["alliance_type"] = 0
                out["severity"] = 1.0

            out["event_type"] = "alliance"
            out = out.dropna(subset=["year_val"])

            if country:
                out = out[out["country_code"].str.upper() == country.upper()]
            if alliance_type:
                out = out[out["alliance_type"] == alliance_type]
            if year_from:
                out = out[out["year_end"] >= year_from]
            if year_to:
                out = out[out["year_val"] <= year_to]
            return out.reset_index(drop=True)

        df = self._cached(cache_params, _fetch, force=force)
        if df.empty:
            return df
        return self._to_canonical(df) if normalize else df

    def _to_canonical(self, df: pd.DataFrame) -> pd.DataFrame:
        if df.empty:
            return df
        out = pd.DataFrame()
        out["event_id"] = df["country_code"] + "_" + df["year_val"].astype(str)
        out["date"] = pd.to_datetime(df["year_val"].astype(str) + "-01-01", errors="coerce")
        out["country_iso3"] = df["country_code"].str.upper().str[:3]
        out["event_type"] = df["event_type"]
        out["severity"] = pd.to_numeric(df["severity"], errors="coerce")
        out["lat"] = None
        out["lon"] = None
        out["source"] = "COW Alliances"
        return out.dropna(subset=["event_id"]).reset_index(drop=True)
