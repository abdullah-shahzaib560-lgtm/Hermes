import logging
from datetime import timedelta
from pathlib import Path
from typing import Optional

import pandas as pd
import urllib.request

from hermes.core.cache import RawCache

logger = logging.getLogger(__name__)

VDEM_URL = (
    "https://github.com/vdeminstitute/vdemdata/raw/main/data/raw/"
    "V-Dem-CY-Core-v16.rds"
)
VDEM_CSV_URL = (
    "https://github.com/vdeminstitute/vdemdata/raw/main/data/raw/"
    "V-Dem-CY-Core-v16.csv"
)

VDEM_INDICATORS = [
    "v2x_polyarchy",
    "v2x_regime",
    "v2x_corr",
    "v2x_clphy",
    "v2x_freexp_altinf",
    "v2x_civlib",
    "v2x_partipdem",
    "v2x_libdem",
    "v2x_delibdem",
]

COUNTRY_COLS = ["country_name", "country_text_id", "COWcode"]


class V_DEM:
    def __init__(self, cache: RawCache | None = None, data_dir: str | None = None):
        self._cache = cache
        self._data_dir = Path(data_dir) if data_dir else (Path.home() / ".hermes_cache" / "vdem")
        self._data_dir.mkdir(parents=True, exist_ok=True)
        self._df: pd.DataFrame | None = None

    def _download_csv(self) -> pd.DataFrame:
        csv_path = self._data_dir / "vdem.csv"
        if csv_path.exists():
            age = pd.Timestamp.now() - pd.Timestamp.fromtimestamp(csv_path.stat().st_mtime)
            if age < timedelta(days=7):
                logger.info("Loading V-DEM from local CSV cache")
                return pd.read_csv(csv_path, low_memory=False)

        logger.info("Downloading V-DEM dataset (~200MB)")
        req = urllib.request.Request(VDEM_CSV_URL, headers={"User-Agent": "Hermes/0.1"})
        with urllib.request.urlopen(req, timeout=300) as resp:
            with open(csv_path, "wb") as f:
                f.write(resp.read())
        logger.info(f"V-DEM CSV saved to {csv_path}")
        return pd.read_csv(csv_path, low_memory=False)

    def _load(self, force: bool = False) -> pd.DataFrame:
        if self._df is not None and not force:
            return self._df
        raw = self._download_csv()
        keep_cols = ["country_text_id", "year"] + VDEM_INDICATORS
        available = [c for c in keep_cols if c in raw.columns]
        df = raw[available].copy()
        df = df.rename(columns={"country_text_id": "country"})
        for ind in VDEM_INDICATORS:
            if ind in df.columns:
                df[ind] = pd.to_numeric(df[ind], errors="coerce")
        df = df.dropna(subset=VDEM_INDICATORS, how="all")
        self._df = df
        return df

    def get_data(
        self,
        indicator: str = "v2x_polyarchy",
        country: Optional[str] = None,
        year_from: Optional[int] = None,
        year_to: Optional[int] = None,
        normalize: bool = True,
        force: bool = False,
    ) -> pd.DataFrame:
        params = {
            "indicator": indicator, "country": country or "",
            "from": year_from or 0, "to": year_to or 0,
        }

        def _fetch():
            df = self._load(force=force)
            if indicator not in df.columns:
                logger.warning(f"V-DEM indicator {indicator} not found")
                return pd.DataFrame()
            out = df[["country", "year", indicator]].copy()
            out = out.rename(columns={indicator: "value"})
            out["indicator_id"] = indicator

            if country:
                out = out[out["country"].str.upper() == country.upper()]
            if year_from:
                out = out[out["year"] >= year_from]
            if year_to:
                out = out[out["year"] <= year_to]
            return out.reset_index(drop=True)

        df = self._cached(params, _fetch, force=force)
        if df.empty:
            return df
        return self._to_canonical(df) if normalize else df

    def _cached(self, params: dict, fetch_fn, force: bool = False):
        if self._cache is None:
            return fetch_fn()
        return self._cache.get_or_fetch("v_dem", params, fetch_fn, force=force, ttl=timedelta(days=7))

    def _to_canonical(self, df: pd.DataFrame) -> pd.DataFrame:
        if df.empty:
            return df
        out = pd.DataFrame()
        if "year" in df.columns:
            out["year"] = df["year"].astype(int)
        if "country" in df.columns:
            out["country_iso3"] = df["country"].astype(str).str.upper().str[:3]
        if "indicator_id" in df.columns:
            out["indicator_id"] = df["indicator_id"]
        if "value" in df.columns:
            out["value"] = pd.to_numeric(df["value"], errors="coerce")
        out["source"] = "V-DEM"
        return out.dropna(subset=["country_iso3", "indicator_id"]).reset_index(drop=True)
