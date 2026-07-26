import logging
from datetime import timedelta
from pathlib import Path
from typing import Optional

import pandas as pd
import urllib.request

from hermes.core.cache import RawCache

logger = logging.getLogger(__name__)

FSI_URL = "https://fragilestatesindex.org/wp-content/uploads/2023/06/FSI-2023-DOWNLOAD.xlsx"


class FSI:
    def __init__(self, cache: RawCache | None = None, data_dir: str | None = None):
        self._cache = cache
        self._data_dir = Path(data_dir) if data_dir else (Path.home() / ".hermes_cache" / "fsi")
        self._data_dir.mkdir(parents=True, exist_ok=True)

    def _download(self) -> pd.DataFrame:
        xlsx_path = self._data_dir / "fsi.xlsx"
        if xlsx_path.exists():
            age = pd.Timestamp.now() - pd.Timestamp.fromtimestamp(xlsx_path.stat().st_mtime)
            if age < timedelta(days=7):
                return pd.read_excel(xlsx_path)
        req = urllib.request.Request(FSI_URL, headers={"User-Agent": "Hermes/0.1"})
        with urllib.request.urlopen(req, timeout=120) as resp:
            with open(xlsx_path, "wb") as f:
                f.write(resp.read())
        return pd.read_excel(xlsx_path)

    def _cached(self, params: dict, fetch_fn, force: bool = False):
        if self._cache is None:
            return fetch_fn()
        return self._cache.get_or_fetch("fsi", params, fetch_fn, force=force, ttl=timedelta(days=7))

    def get_data(
        self,
        indicator: str = "total",
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
            df = self._download()
            df.columns = [str(c).strip().lower().replace(" ", "_") for c in df.columns]
            country_col = next((c for c in df.columns if "country" in c or "state" in c), None)
            if not country_col:
                return pd.DataFrame()

            iso_col = next((c for c in df.columns if "iso" in c), None)
            year_col = next((c for c in df.columns if "year" in c), None)
            val_col = next((c for c in df.columns if "total" in c or "score" in c), None)

            if not val_col:
                return pd.DataFrame()

            out = pd.DataFrame()
            if iso_col:
                out["country_iso3_raw"] = df[iso_col].astype(str)
            else:
                out["country_iso3_raw"] = df[country_col].astype(str).str.upper().str[:3]
            out["year_val"] = pd.to_numeric(df[year_col], errors="coerce") if year_col else (year or 2024)
            out["value"] = pd.to_numeric(df[val_col], errors="coerce")
            out["indicator_id"] = "fragile_state_" + indicator
            out = out.dropna(subset=["value"])

            if country:
                out = out[out["country_iso3_raw"].str.upper() == country.upper()]
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
        out["country_iso3"] = df["country_iso3_raw"].str.upper().str[:3]
        out["year"] = df["year_val"].astype(int)
        out["indicator_id"] = df["indicator_id"]
        out["value"] = df["value"]
        out["source"] = "Fragile States Index"
        return out.dropna(subset=["country_iso3", "indicator_id"]).reset_index(drop=True)
