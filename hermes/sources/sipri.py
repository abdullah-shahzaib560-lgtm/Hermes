import logging
from datetime import timedelta
from io import StringIO
from pathlib import Path
from typing import Optional

import pandas as pd
import urllib.request

from hermes.core.cache import RawCache

logger = logging.getLogger(__name__)

SIPRI_URL = "https://www.sipri.org/sites/default/files/SIPRI-TIVs-2024.xlsx"


class SIPRI:
    def __init__(self, cache: RawCache | None = None, data_dir: str | None = None):
        self._cache = cache
        self._data_dir = Path(data_dir) if data_dir else (Path.home() / ".hermes_cache" / "sipri")
        self._data_dir.mkdir(parents=True, exist_ok=True)

    def _download(self) -> pd.DataFrame:
        xlsx_path = self._data_dir / "sipri.xlsx"
        if xlsx_path.exists():
            age = pd.Timestamp.now() - pd.Timestamp.fromtimestamp(xlsx_path.stat().st_mtime)
            if age < timedelta(days=7):
                return pd.read_excel(xlsx_path)
        req = urllib.request.Request(SIPRI_URL, headers={"User-Agent": "Hermes/0.1"})
        with urllib.request.urlopen(req, timeout=120) as resp:
            with open(xlsx_path, "wb") as f:
                f.write(resp.read())
        return pd.read_excel(xlsx_path)

    def _cached(self, params: dict, fetch_fn, force: bool = False):
        if self._cache is None:
            return fetch_fn()
        return self._cache.get_or_fetch("sipri", params, fetch_fn, force=force, ttl=timedelta(days=7))

    def get_data(
        self,
        indicator: str = "imports",
        country: Optional[str] = None,
        year_from: Optional[int] = None,
        year_to: Optional[int] = None,
        normalize: bool = True,
        force: bool = False,
    ) -> pd.DataFrame:
        cache_params = {
            "q": "get_data", "indicator": indicator, "country": country or "",
            "from": year_from or 0, "to": year_to or 0,
        }

        def _fetch():
            df = self._download()
            df.columns = [str(c).strip().lower().replace(" ", "_") for c in df.columns]
            supplier_col = next((c for c in df.columns if "supplier" in c), None)
            recipient_col = next((c for c in df.columns if "recipient" in c), None)
            year_col = next((c for c in df.columns if "year" in c), None)
            tiv_col = next((c for c in df.columns if "tiv" in c or "value" in c or "total" in c), None)

            if not (supplier_col and recipient_col and tiv_col):
                return pd.DataFrame()

            out = pd.DataFrame()
            if indicator == "imports":
                out["country_iso3_raw"] = df[recipient_col].astype(str)
                out["partner"] = df[supplier_col].astype(str)
            else:
                out["country_iso3_raw"] = df[supplier_col].astype(str)
                out["partner"] = df[recipient_col].astype(str)

            if year_col:
                out["year_val"] = pd.to_numeric(df[year_col], errors="coerce")
            else:
                out["year_val"] = 2023

            out["value"] = pd.to_numeric(df[tiv_col], errors="coerce")
            out["indicator_id"] = "arms_" + indicator
            out = out.dropna(subset=["value"])

            if country:
                out = out[out["country_iso3_raw"].str.upper() == country.upper()]
            if year_from:
                out = out[out["year_val"] >= year_from]
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
        out["country_iso3"] = df["country_iso3_raw"].str.upper().str[:3]
        out["year"] = df["year_val"].astype(int)
        out["indicator_id"] = df["indicator_id"]
        out["value"] = pd.to_numeric(df["value"], errors="coerce")
        out["source"] = "SIPRI"
        return out.dropna(subset=["country_iso3", "indicator_id"]).reset_index(drop=True)
