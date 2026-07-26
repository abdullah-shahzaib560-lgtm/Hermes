import logging
from datetime import timedelta
from io import StringIO
from typing import Optional

import pandas as pd
import urllib.request

from hermes.core.cache import RawCache

logger = logging.getLogger(__name__)

SDMX_BASE = "https://stats.bis.org/api/v2"


def _dim_key(*parts: str) -> str:
    return ".".join(parts) if parts else ""


class BIS:
    FLOWS = {
        "cb_rates": {"ref": "BIS/WS_CBPOL/1.0", "desc": "Central bank policy rates",
                      "key_fn": lambda country: _dim_key("M", country)},
        "eer": {"ref": "BIS/WS_EER/1.0", "desc": "Effective exchange rates",
                "key_fn": lambda country: _dim_key("M", "N", "B", country)},
        "xru": {"ref": "BIS/WS_XRU/1.0", "desc": "US dollar exchange rates",
                "key_fn": lambda country: _dim_key("M", country)},
        "spp": {"ref": "BIS/WS_SPP/1.0", "desc": "Residential property prices",
                "key_fn": lambda country: _dim_key("Q", country)},
        "cbta": {"ref": "BIS/WS_CBTA/1.0", "desc": "Central bank total assets",
                 "key_fn": lambda country: _dim_key("Q", country)},
        "cpi": {"ref": "BIS/WS_LONG_CPI/1.0", "desc": "Consumer prices",
                "key_fn": lambda country: _dim_key("M", country)},
        "credit_gap": {"ref": "BIS/WS_CREDIT_GAP/1.0", "desc": "Credit-to-GDP gaps",
                       "key_fn": lambda country: _dim_key("Q", country)},
        "total_credit": {"ref": "BIS/WS_TC/2.0", "desc": "Total credit to non-financial sector",
                         "key_fn": lambda country, sector="C": _dim_key("Q", country, sector, "A", "M", "770", "A")},
        "debt_securities": {"ref": "BIS/WS_DEBT_SEC2_PUB/1.0", "desc": "International debt securities",
                            "key_fn": lambda country: _dim_key("Q", country, "A", "A", "A", "A", "A", "A", "A", "A", "A", "A", "A", "A", "A")},
        "locational_banking": {"ref": "BIS/WS_LBS_D_PUB/1.0", "desc": "Locational banking statistics",
                               "key_fn": lambda country: _dim_key("Q", country)},
        "consolidated_banking": {"ref": "BIS/WS_CBS_PUB/1.0", "desc": "Consolidated banking statistics",
                                 "key_fn": lambda country: _dim_key("Q", country)},
    }

    def __init__(self, cache: RawCache | None = None):
        self._cache = cache

    def _fetch_csv(self, url: str) -> str:
        req = urllib.request.Request(url, headers={"Accept": "text/csv", "User-Agent": "Hermes/0.1"})
        with urllib.request.urlopen(req, timeout=60) as resp:
            return resp.read().decode()

    def _cached(self, params: dict, fetch_fn, force: bool = False):
        if self._cache is None:
            return fetch_fn()
        return self._cache.get_or_fetch("bis", params, fetch_fn, force=force, ttl=timedelta(hours=24))

    def get_data(
        self,
        flow: str = "total_credit",
        country: str = "",
        start_period: Optional[str] = None,
        end_period: Optional[str] = None,
        normalize: bool = True,
        force: bool = False,
    ) -> pd.DataFrame:
        info = self.FLOWS.get(flow)
        if info is None:
            raise ValueError(f"Unknown flow '{flow}'. Known: {list(self.FLOWS.keys())}")

        cache_params = {
            "q": "get_data", "flow": flow, "country": country or "",
            "start": start_period or "", "end": end_period or "",
        }

        def _fetch():
            params_dict = {"format": "csv"}
            if start_period:
                params_dict["startPeriod"] = start_period
            if end_period:
                params_dict["endPeriod"] = end_period

            key = info["key_fn"](country) if country else ""
            qs = "&".join(f"{k}={v}" for k, v in params_dict.items())
            url = f"{SDMX_BASE}/data/dataflow/{info['ref']}/{key}?{qs}" if key else f"{SDMX_BASE}/data/dataflow/{info['ref']}?{qs}"
            raw = self._fetch_csv(url)
            return pd.read_csv(StringIO(raw))

        df = self._cached(cache_params, _fetch, force=force)
        if df.empty:
            return df
        return self._to_canonical(df) if normalize else df

    def get_cb_policy_rates(self, country: str = "", normalize: bool = True, force: bool = False) -> pd.DataFrame:
        return self.get_data(flow="cb_rates", country=country, normalize=normalize, force=force)

    def get_eer(self, country: str = "", normalize: bool = True, force: bool = False) -> pd.DataFrame:
        return self.get_data(flow="eer", country=country, normalize=normalize, force=force)

    def get_exchange_rates(self, country: str = "", normalize: bool = True, force: bool = False) -> pd.DataFrame:
        return self.get_data(flow="xru", country=country, normalize=normalize, force=force)

    def get_property_prices(self, country: str = "", normalize: bool = True, force: bool = False) -> pd.DataFrame:
        return self.get_data(flow="spp", country=country, normalize=normalize, force=force)

    def get_central_bank_assets(self, country: str = "", normalize: bool = True, force: bool = False) -> pd.DataFrame:
        return self.get_data(flow="cbta", country=country, normalize=normalize, force=force)

    def get_cpi(self, country: str = "", normalize: bool = True, force: bool = False) -> pd.DataFrame:
        return self.get_data(flow="cpi", country=country, normalize=normalize, force=force)

    def get_credit_gap(self, country: str = "", normalize: bool = True, force: bool = False) -> pd.DataFrame:
        return self.get_data(flow="credit_gap", country=country, normalize=normalize, force=force)

    def get_total_credit(self, country: str = "", sector: str = "C", normalize: bool = True, force: bool = False) -> pd.DataFrame:
        return self.get_data(flow="total_credit", country=country, normalize=normalize, force=force)

    def get_debt_securities(self, country: str = "", normalize: bool = True, force: bool = False) -> pd.DataFrame:
        return self.get_data(flow="debt_securities", country=country, normalize=normalize, force=force)

    def get_locational_banking(self, country: str = "", normalize: bool = True, force: bool = False) -> pd.DataFrame:
        return self.get_data(flow="locational_banking", country=country, normalize=normalize, force=force)

    def get_consolidated_banking(self, country: str = "", normalize: bool = True, force: bool = False) -> pd.DataFrame:
        return self.get_data(flow="consolidated_banking", country=country, normalize=normalize, force=force)

    def _to_canonical(self, df: pd.DataFrame) -> pd.DataFrame:
        if df.empty:
            return df
        out = pd.DataFrame()
        time_col = next((c for c in df.columns if c == "TIME_PERIOD"), None)
        if time_col:
            out["date"] = pd.to_datetime(df[time_col].astype(str).str[:10], errors="coerce")

        area_col = next((c for c in df.columns if c in ("REF_AREA", "BORROWERS_CTY", "ISSUER_RES")), None)
        if area_col:
            out["country_iso3"] = df[area_col].astype(str).str.upper().str[:3]

        val_col = next((c for c in df.columns if c == "OBS_VALUE"), None)
        if val_col:
            out["value"] = pd.to_numeric(df[val_col], errors="coerce")

        title_col = next((c for c in df.columns if c in ("TITLE_TS", "TITLE")), None)
        if title_col:
            out["indicator_id"] = df[title_col].astype(str)
        else:
            out["indicator_id"] = flow_name = "bis_flow"

        out["source"] = "BIS"
        for col in ["date", "country_iso3", "indicator_id", "value"]:
            if col not in out.columns:
                out[col] = None
        return out.dropna(subset=["date", "country_iso3", "value"]).reset_index(drop=True)
