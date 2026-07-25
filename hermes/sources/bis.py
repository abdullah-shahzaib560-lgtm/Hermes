import pandas as pd
import logging
import httpx
from typing import Optional
from io import StringIO

from hermes.core.cache import RawCache

logger = logging.getLogger(__name__)

SDMX_BASE = "https://stats.bis.org/api/v2"


class BIS:
    STAT_CATEGORIES = {
        "ws_bank": "WS_BANK",
        "ws_credit": "WS_CREDIT",
        "ws_property": "WS_PROPERTY",
        "ws_debt": "WS_DEBT",
        "ws_fx": "WS_FX",
    }

    def __init__(self, cache: RawCache | None = None):
        self.base_url = SDMX_BASE
        self._cache = cache

    def _cached(self, params: dict, fetch_fn, force: bool = False):
        if self._cache is None:
            return fetch_fn()
        return self._cache.get_or_fetch("bis", params, fetch_fn, force=force)

    def get_data(
        self,
        category: str = "ws_credit",
        indicator: Optional[str] = None,
        country: str = "all",
        start_period: Optional[str] = None,
        end_period: Optional[str] = None,
        normalize: bool = True,
        force: bool = False,
    ) -> pd.DataFrame:
        cache_params = {
            "action": "get_data",
            "category": category,
            "indicator": indicator or "",
            "country": country,
            "start_period": start_period or "",
            "end_period": end_period or "",
        }

        def _fetch():
            cat = self.STAT_CATEGORIES.get(category, category)
            if indicator:
                key = f"{cat}/{indicator}"
            else:
                key = cat

            params = {}
            if start_period:
                params["startPeriod"] = start_period
            if end_period:
                params["endPeriod"] = end_period

            url = f"{self.base_url}/data/{key}"
            resp = httpx.get(
                url, params=params, timeout=60,
                headers={"Accept": "text/csv"},
            )
            resp.raise_for_status()
            return pd.read_csv(StringIO(resp.text))

        df = self._cached(cache_params, _fetch, force=force)
        if df.empty:
            return df
        return self._to_canonical(df) if normalize else df

    def get_banking_stats(
        self, country: str = "all", normalize: bool = True
    ) -> pd.DataFrame:
        return self.get_data(category="ws_bank", country=country, normalize=normalize)

    def get_credit_aggregates(
        self, country: str = "all", normalize: bool = True
    ) -> pd.DataFrame:
        return self.get_data(category="ws_credit", country=country, normalize=normalize)

    def get_property_prices(
        self, country: str = "all", normalize: bool = True
    ) -> pd.DataFrame:
        return self.get_data(category="ws_property", country=country, normalize=normalize)

    def get_debt_securities(
        self, country: str = "all", normalize: bool = True
    ) -> pd.DataFrame:
        return self.get_data(category="ws_debt", country=country, normalize=normalize)

    def get_fx_liquidity(
        self, country: str = "all", normalize: bool = True
    ) -> pd.DataFrame:
        return self.get_data(category="ws_fx", country=country, normalize=normalize)

    def _to_canonical(self, df: pd.DataFrame) -> pd.DataFrame:
        out = pd.DataFrame()
        date_col = df.get("TIME_PERIOD", df.get("Period", pd.NA))
        if not date_col.isna().all():
            out["date"] = pd.to_datetime(date_col, errors="coerce")

        country_col = df.get(
            "REF_AREA", df.get("BorrowingCountry", df.get("Country", pd.NA))
        )
        if not country_col.isna().all():
            out["country_iso3"] = country_col.astype(str).str.upper()

        indicator_col = df.get(
            "INDICATOR", df.get("SERIES_CODE", df.get("Series", pd.NA))
        )
        if not indicator_col.isna().all():
            out["indicator_id"] = indicator_col

        value_col = df.get("OBS_VALUE", df.get("Value", df.get("Amount", pd.NA)))
        if not value_col.isna().all():
            out["value"] = pd.to_numeric(value_col, errors="coerce")

        out["source"] = "BIS"
        return out.dropna(subset=["date", "value"])
