import pandas as pd
import logging
import urllib.request
import urllib.parse
import json
from typing import Optional

from hermes.core.cache import RawCache

logger = logging.getLogger(__name__)

PUBLIC_BASE = "https://comtradeapi.un.org/public/v1"
DATA_BASE = "https://comtradeapi.un.org/data/v1"

COUNTRY_TO_COMTRADE = {
    "CHN": "156", "USA": "842", "GBR": "826", "DEU": "276", "FRA": "250",
    "ITA": "380", "JPN": "392", "CAN": "124", "AUS": "36", "RUS": "643",
    "BRA": "76", "IND": "699", "ZAF": "710", "MEX": "484", "KOR": "410",
    "TUR": "792", "IDN": "360", "SAU": "682", "CHE": "756", "NLD": "528",
    "ESP": "724", "SWE": "752", "NOR": "578", "POL": "616", "DNK": "208",
    "UKR": "804", "ARG": "32", "IRN": "364", "IRQ": "368", "ISR": "376",
    "EGY": "818", "NGA": "566", "PAK": "586", "THA": "764", "VNM": "704",
    "MYS": "458", "SGP": "702", "PHL": "608",     "HKG": "344", "TWN": "490", "ARE": "784", "COL": "170",
    "CHL": "152", "PER": "604", "ROU": "642", "CZE": "203",
    "HUN": "348", "PRT": "620", "GRC": "300", "FIN": "246",
    "AUT": "40", "BEL": "56", "BLR": "112", "KAZ": "398",
    "XKX": "688", "SRB": "688",
}


def _comtrade_code(code: str) -> str:
    return COUNTRY_TO_COMTRADE.get(code.upper(), code)


class Comtrade:
    def __init__(self, api_key: Optional[str] = None, cache: RawCache | None = None):
        self.api_key = api_key
        self._cache = cache

    def _fetch_json(self, url: str) -> dict:
        req = urllib.request.Request(url, headers={"User-Agent": "Hermes/0.1"})
        with urllib.request.urlopen(req, timeout=60) as resp:
            return json.loads(resp.read().decode())

    def _cached(self, params: dict, fetch_fn, force: bool = False):
        if self._cache is None:
            return fetch_fn()
        return self._cache.get_or_fetch("comtrade", params, fetch_fn, force=force)

    def get_data(
        self,
        freq: str = "A",
        reporter: str = "all",
        partner: str = "0",
        commodity: str = "TOTAL",
        flow: Optional[str] = None,
        period: Optional[str] = None,
        classification: str = "HS",
        normalize: bool = True,
        force: bool = False,
    ) -> pd.DataFrame:
        cache_params = {
            "q": "get_data", "freq": freq, "reporter": reporter,
            "partner": partner, "commodity": commodity, "flow": flow or "",
            "period": period or "", "cls": classification,
        }

        def _fetch():
            if self.api_key:
                # data/v1/get/{type}/{freq}/{clCode}?reporterCode=... requires subscription-key
                endpoint = f"{DATA_BASE}/get/{'C'}/{freq}/{classification}"
            else:
                # public/v1/preview/{type}/{freq}/{clCode}?reporterCode=...
                endpoint = f"{PUBLIC_BASE}/preview/{'C'}/{freq}/{classification}"

            params = {
                "reporterCode": _comtrade_code(reporter),
                "partnerCode": _comtrade_code(partner),
                "cmdCode": commodity,
                "period": period or "2024",
                "maxRecords": 500,
            }
            if flow:
                params["flowCode"] = flow
            if self.api_key:
                params["subscription-key"] = self.api_key

            qs = "&".join(f"{k}={urllib.parse.quote(str(v))}" for k, v in params.items())
            url = f"{endpoint}?{qs}"
            data = self._fetch_json(url)
            rows = data.get("data", data.get("dataset", []))
            return pd.DataFrame(rows)

        df = self._cached(cache_params, _fetch, force=force)
        if df.empty:
            return df
        return self._to_canonical(df) if normalize else df

    def get_bilateral_trade(
        self,
        origin: str,
        destination: str,
        freq: str = "A",
        commodity: str = "TOTAL",
        period: Optional[str] = None,
        normalize: bool = True,
        force: bool = False,
    ) -> pd.DataFrame:
        return self.get_data(
            freq=freq, reporter=origin, partner=destination,
            commodity=commodity, period=period,
            normalize=normalize, force=force,
        )

    def _to_canonical(self, df: pd.DataFrame) -> pd.DataFrame:
        out = pd.DataFrame()
        period_cols = [c for c in df.columns if c.lower() in ("period", "yr", "year", "perioddesc")]
        for c in period_cols:
            if c in df.columns and not df[c].isna().all():
                out["date"] = pd.to_datetime(df[c].astype(str).str[:10], errors="coerce")
                break
        if "date" not in out.columns:
            out["date"] = pd.NaT

        rep_cols = [c for c in df.columns if c.lower() in ("reporteriso", "reportercode", "rtcode")]
        for c in rep_cols:
            if c in df.columns and not df[c].isna().all():
                out["origin_iso3"] = df[c].astype(str).str.upper().str[:3]
                break

        prt_cols = [c for c in df.columns if c.lower() in ("partneriso", "partnercode", "ptcode")]
        for c in prt_cols:
            if c in df.columns and not df[c].isna().all():
                out["destination_iso3"] = df[c].astype(str).str.upper().str[:3]
                break

        cmd_cols = [c for c in df.columns if c.lower() in ("commoditycode", "cmdcode", "cmdcode_HS")]
        for c in cmd_cols:
            if c in df.columns and not df[c].isna().all():
                out["commodity_code"] = df[c].astype(str)
                break

        val_cols = [c for c in df.columns if c.lower() in ("tradevalue", "tradevalueinusd", "tv", "value", "primaryvalue")]
        for c in val_cols:
            if c in df.columns:
                out["value"] = pd.to_numeric(df[c], errors="coerce")
                break

        out["source"] = "UN Comtrade"
        return out.dropna(subset=["value"])
