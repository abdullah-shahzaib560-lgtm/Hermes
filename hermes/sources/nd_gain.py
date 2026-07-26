import logging
from datetime import timedelta
from pathlib import Path
from typing import Optional

import pandas as pd
import urllib.request

from hermes.core.cache import RawCache

logger = logging.getLogger(__name__)

NDGAIN_ZIP_URL = "https://gain.nd.edu/assets/647440/ndgain_countryindex_2026.zip"


class ND_GAIN:
    def __init__(self, cache: RawCache | None = None, data_dir: str | None = None):
        self._cache = cache
        self._data_dir = Path(data_dir) if data_dir else (Path.home() / ".hermes_cache" / "ndgain")
        self._data_dir.mkdir(parents=True, exist_ok=True)

    def _download_csv(self) -> pd.DataFrame:
        csv_path = self._data_dir / "ndgain.csv"
        if csv_path.exists():
            age = pd.Timestamp.now() - pd.Timestamp.fromtimestamp(csv_path.stat().st_mtime)
            if age < timedelta(days=7):
                return pd.read_csv(csv_path)

        req = urllib.request.Request(NDGAIN_ZIP_URL, headers={"User-Agent": "Hermes/0.1"})
        with urllib.request.urlopen(req, timeout=120) as resp:
            with open(csv_path, "wb") as f:
                f.write(resp.read())
        return pd.read_csv(csv_path)

    def _cached(self, params: dict, fetch_fn, force: bool = False):
        if self._cache is None:
            return fetch_fn()
        return self._cache.get_or_fetch("nd_gain", params, fetch_fn, force=force, ttl=timedelta(days=7))

    def get_data(
        self,
        indicator: str = "vulnerability",
        country: Optional[str] = None,
        year: Optional[int] = None,
        normalize: bool = True,
        force: bool = False,
    ) -> pd.DataFrame:
        cache_params = {
            "q": "get_data", "indicator": indicator, "country": country or "",
            "year": year or 0,
        }

        def _fetch():
            df = self._download_csv()
            df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

            iso_col = next((c for c in df.columns if "iso" in c), None)
            if not iso_col:
                iso_col = next((c for c in df.columns if c in ("country_code", "code", "cc")), None)
            if not iso_col:
                return pd.DataFrame()

            col_map = {
                "vulnerability": ["vulnerability", "vuln", "vulnerability_score"],
                "readiness": ["readiness", "readiness_score", "ready"],
                "exposure": ["exposure"],
                "sensitivity": ["sensitivity"],
                "adaptive_capacity": ["adaptive_capacity", "adaptivecapacity"],
            }
            candidates = col_map.get(indicator, [indicator])
            val_col = next((c for c in candidates if c in df.columns), None)
            if not val_col:
                logger.warning(f"ND-GAIN indicator {indicator} not found in columns: {list(df.columns)}")
                return pd.DataFrame()

            year_col = next((c for c in df.columns if "year" in c), None)
            out = pd.DataFrame()
            out["country_raw"] = df[iso_col].astype(str)
            if year_col:
                out["year_val"] = pd.to_numeric(df[year_col], errors="coerce")
            else:
                out["year_val"] = year or 2023
            out["value"] = pd.to_numeric(df[val_col], errors="coerce")
            out["indicator_id"] = indicator
            out = out.dropna(subset=["value"])

            if country:
                out = out[out["country_raw"].str.upper() == country.upper()]
            if year:
                out = out[out["year_val"] == year]
            return out.reset_index(drop=True)

        df = self._cached(cache_params, _fetch, force=force)
        if df.empty:
            return df
        return self._to_canonical(df) if normalize else df

    def _to_canonical(self, df: pd.DataFrame) -> pd.DataFrame:
        if df.empty:
            return df
        out = pd.DataFrame()
        out["country_iso3"] = df["country_raw"].str.upper().str[:3]
        out["year"] = df["year_val"].astype(int)
        out["indicator_id"] = df["indicator_id"]
        out["value"] = df["value"]
        out["source"] = "ND-GAIN"
        return out.dropna(subset=["country_iso3", "indicator_id"]).reset_index(drop=True)
