import logging
from datetime import timedelta
from pathlib import Path
from typing import Optional

import pandas as pd
import urllib.request

from hermes.core.cache import RawCache

logger = logging.getLogger(__name__)

HDI_URL = "https://hdr.undp.org/sites/default/files/2025_HDR/HDR25_Composite_indices_complete_time_series.csv"


class UNDP:
    def __init__(self, cache: RawCache | None = None, data_dir: str | None = None):
        self._cache = cache
        self._data_dir = Path(data_dir) if data_dir else (Path.home() / ".hermes_cache" / "undp")
        self._data_dir.mkdir(parents=True, exist_ok=True)

    def _download_csv(self) -> pd.DataFrame:
        csv_path = self._data_dir / "hdi.csv"
        if csv_path.exists():
            age = pd.Timestamp.now() - pd.Timestamp.fromtimestamp(csv_path.stat().st_mtime)
            if age < timedelta(days=7):
                return pd.read_csv(csv_path, encoding='latin1')

        req = urllib.request.Request(HDI_URL, headers={"User-Agent": "Hermes/0.1"})
        with urllib.request.urlopen(req, timeout=120) as resp:
            with open(csv_path, "wb") as f:
                f.write(resp.read())
        return pd.read_csv(csv_path, encoding='latin1')

    def _cached(self, params: dict, fetch_fn, force: bool = False):
        if self._cache is None:
            return fetch_fn()
        return self._cache.get_or_fetch("undp", params, fetch_fn, force=force, ttl=timedelta(days=7))

    def get_data(
        self,
        indicator: str = "hdi",
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
            df = self._download_csv()
            df.columns = [c.strip() for c in df.columns]
            iso_col = next((c for c in df.columns if "iso" in c.lower()), None)
            if not iso_col:
                return pd.DataFrame()

            prefix = indicator.lower() + "_"
            year_cols = sorted(c for c in df.columns if c.lower().startswith(prefix) and c.split("_")[-1].isdigit())
            if not year_cols:
                return pd.DataFrame()

            id_vars = [iso_col]
            out = df[id_vars + year_cols].melt(id_vars=id_vars, var_name="year_raw", value_name="value")
            out["country_iso3_raw"] = out[iso_col].astype(str).str.upper()
            out["year"] = out["year_raw"].str.replace(prefix, "").astype(int)
            out["value"] = pd.to_numeric(out["value"], errors="coerce")
            out["indicator_id"] = indicator
            out = out.dropna(subset=["value", "year"])

            if country:
                out = out[out["country_iso3_raw"] == country.upper()]
            if year_from:
                out = out[out["year"] >= year_from]
            if year_to:
                out = out[out["year"] <= year_to]
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
        out["year"] = df["year"].astype(int)
        out["indicator_id"] = df["indicator_id"]
        out["value"] = df["value"]
        out["source"] = "UNDP"
        return out.dropna(subset=["country_iso3", "indicator_id"]).reset_index(drop=True)
