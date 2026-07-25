import pandas as pd
import logging
import urllib.request
from typing import Optional
from io import StringIO

from hermes.core.cache import RawCache

logger = logging.getLogger(__name__)

SDMX_BASE = "https://stats.bis.org/api/v2"


def _dim_key(*parts: str) -> str:
    return ".".join(parts) if parts else ""


class BIS:
    FLOWS = {
        "cb_rates": {
            "ref": "BIS/WS_CBPOL/1.0",
            "version": 1.0,
            "desc": "Central bank policy rates",
            "key_fn": lambda country: _dim_key("M", country),
        },
        "eer": {
            "ref": "BIS/WS_EER/1.0",
            "version": 1.0,
            "desc": "Effective exchange rates",
            "key_fn": lambda country: _dim_key("M", "N", "B", country),
        },
        "xru": {
            "ref": "BIS/WS_XRU/1.0",
            "version": 1.0,
            "desc": "US dollar exchange rates",
            "key_fn": lambda country: _dim_key("M", country),
        },
        "spp": {
            "ref": "BIS/WS_SPP/1.0",
            "version": 1.0,
            "desc": "Selected residential property prices",
            "key_fn": lambda country: _dim_key("Q", country),
        },
        "cbta": {
            "ref": "BIS/WS_CBTA/1.0",
            "version": 1.0,
            "desc": "Central bank total assets",
            "key_fn": lambda country: _dim_key("Q", country),
        },
        "cpi": {
            "ref": "BIS/WS_LONG_CPI/1.0",
            "version": 1.0,
            "desc": "Consumer prices statistics",
            "key_fn": lambda country: _dim_key("M", country),
        },
        "credit_gap": {
            "ref": "BIS/WS_CREDIT_GAP/1.0",
            "version": 1.0,
            "desc": "Credit-to-GDP gaps",
            "key_fn": lambda country: _dim_key("Q", country),
        },
        "otc_derivatives": {
            "ref": "BIS/WS_OTC_DERIV2/1.0",
            "version": 1.0,
            "desc": "OTC derivatives outstanding",
            "key_fn": lambda country: _dim_key("Q", country, "A", "A", "A", "A", "A", "A", "A", "A", "A", "A"),
        },
        "xtd_derivatives": {
            "ref": "BIS/WS_XTD_DERIV/1.0",
            "version": 1.0,
            "desc": "Exchange-traded derivatives",
            "key_fn": lambda country: _dim_key("Q", country),
        },
        "total_credit": {
            "ref": "BIS/WS_TC/2.0",
            "version": 2.0,
            "desc": "Total credit to non-financial sector",
            "key_fn": lambda country, sector="C": _dim_key("Q", country, sector, "A", "M", "770", "A"),
        },
        "credit_gap_v2": {
            "ref": "BIS/WS_CREDIT_GAP/2.0",
            "version": 2.0,
            "desc": "Credit-to-GDP gaps v2",
            "key_fn": lambda country, sector="P": _dim_key("Q", country, sector, "A", "A"),
        },
        "debt_securities": {
            "ref": "BIS/WS_DEBT_SEC2_PUB/1.0",
            "version": 1.0,
            "desc": "International debt securities (BIS-compiled)",
            "key_fn": lambda country: _dim_key("Q", country, "A", "A", "A", "A", "A", "A", "A", "A", "A", "A", "A", "A", "A"),
        },
        "locational_banking": {
            "ref": "BIS/WS_LBS_D_PUB/1.0",
            "version": 1.0,
            "desc": "Locational banking statistics",
            "key_fn": lambda country: _dim_key("Q", country),
        },
        "consolidated_banking": {
            "ref": "BIS/WS_CBS_PUB/1.0",
            "version": 1.0,
            "desc": "Consolidated banking statistics",
            "key_fn": lambda country: _dim_key("Q", country),
        },
    }

    def __init__(self, cache: RawCache | None = None):
        self._cache = cache

    def _fetch_csv(self, url: str) -> str:
        req = urllib.request.Request(url, headers={"Accept": "text/csv"})
        with urllib.request.urlopen(req, timeout=60) as resp:
            return resp.read().decode()

    def _cached(self, params: dict, fetch_fn, force: bool = False):
        if self._cache is None:
            return fetch_fn()
        return self._cache.get_or_fetch("bis", params, fetch_fn, force=force)

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
        info = self.FLOWS["total_credit"]
        cache_params = {
            "q": "get_total_credit", "country": country or "",
            "sector": sector, "start": "", "end": "",
        }

        def _fetch():
            key = _dim_key("Q", country, sector, "A", "M", "770", "A")
            url = f"{SDMX_BASE}/data/dataflow/{info['ref']}/{key}?format=csv"
            raw = self._fetch_csv(url)
            return pd.read_csv(StringIO(raw))

        df = self._cached(cache_params, _fetch, force=force)
        if df.empty:
            return df
        return self._to_canonical(df) if normalize else df

    def get_otc_derivatives(self, country: str = "", normalize: bool = True, force: bool = False) -> pd.DataFrame:
        return self.get_data(flow="otc_derivatives", country=country, normalize=normalize, force=force)

    def get_xtd_derivatives(self, country: str = "", normalize: bool = True, force: bool = False) -> pd.DataFrame:
        return self.get_data(flow="xtd_derivatives", country=country, normalize=normalize, force=force)

    def get_debt_securities(self, country: str = "", normalize: bool = True, force: bool = False) -> pd.DataFrame:
        return self.get_data(flow="debt_securities", country=country, normalize=normalize, force=force)

    def get_locational_banking(self, country: str = "", normalize: bool = True, force: bool = False) -> pd.DataFrame:
        return self.get_data(flow="locational_banking", country=country, normalize=normalize, force=force)

    def get_consolidated_banking(self, country: str = "", normalize: bool = True, force: bool = False) -> pd.DataFrame:
        return self.get_data(flow="consolidated_banking", country=country, normalize=normalize, force=force)

    def _to_canonical(self, df: pd.DataFrame) -> pd.DataFrame:
        out = pd.DataFrame()
        time_cols = [c for c in df.columns if c == "TIME_PERIOD"]
        if time_cols:
            raw = df[time_cols[0]].astype(str).str[:10]
            out["date"] = pd.to_datetime(raw, errors="coerce")

        area_cols = [c for c in df.columns if c in ("REF_AREA", "BORROWERS_CTY", "ISSUER_RES")]
        for c in area_cols:
            if c in df.columns and not df[c].isna().all():
                out["country_iso3"] = df[c].astype(str).str.upper().str[:3]
                break

        val_cols = [c for c in df.columns if c == "OBS_VALUE"]
        for c in val_cols:
            if c in df.columns:
                out["value"] = pd.to_numeric(df[c], errors="coerce")
                break

        title_col = [c for c in df.columns if c in ("TITLE_TS", "TITLE")]
        if title_col and title_col[0] in df.columns:
            out["indicator_id"] = df[title_col[0]].astype(str)

        out["source"] = "BIS"
        return out.dropna(subset=["date", "value"])
