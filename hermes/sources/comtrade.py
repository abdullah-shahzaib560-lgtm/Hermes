import pandas as pd
import logging
import httpx
from typing import Optional

from hermes.core.cache import RawCache

logger = logging.getLogger(__name__)

V1_BASE = "https://comtradeapi.un.gov/api/v1"
V2_BASE = "https://comtradeapi.un.gov/api/v2"


class Comtrade:
    def __init__(self, api_key: Optional[str] = None, cache: RawCache | None = None):
        self.api_key = api_key
        self._cache = cache

    def _cached(self, params: dict, fetch_fn, force: bool = False):
        if self._cache is None:
            return fetch_fn()
        return self._cache.get_or_fetch("comtrade", params, fetch_fn, force=force)

    def get_trade_data_v1(
        self,
        freq: str = "A",
        reporter: Optional[str] = None,
        partner: Optional[str] = None,
        commodity: str = "TOTAL",
        flow: Optional[str] = None,
        period: Optional[str] = None,
        normalize: bool = True,
        force: bool = False,
    ) -> pd.DataFrame:
        cache_params = {
            "action": "get_trade_data_v1",
            "freq": freq,
            "reporter": reporter or "all",
            "partner": partner or "0",
            "commodity": commodity,
            "flow": flow or "",
            "period": period or "now",
        }

        def _fetch():
            params = {
                "type": "C",
                "freq": freq,
                "px": "HS",
                "ps": period or "now",
                "r": reporter or "all",
                "p": partner or "0",
                "cc": commodity,
                "fmt": "json",
            }
            if flow:
                params["rg"] = flow
            if self.api_key:
                params["api_key"] = self.api_key

            url = f"{V1_BASE}/get"
            resp = httpx.get(url, params=params, timeout=60)
            resp.raise_for_status()
            data = resp.json()
            return pd.DataFrame(data.get("dataset", []))

        df = self._cached(cache_params, _fetch, force=force)
        if df.empty:
            return df
        return self._to_canonical(df) if normalize else df

    def get_trade_data_v2(
        self,
        freq: str = "A",
        reporter: Optional[str] = None,
        partner: Optional[str] = None,
        commodity: str = "TOTAL",
        flow: Optional[str] = None,
        period: Optional[str] = None,
        normalize: bool = True,
        force: bool = False,
    ) -> pd.DataFrame:
        cache_params = {
            "action": "get_trade_data_v2",
            "freq": freq,
            "reporter": reporter or "all",
            "partner": partner or "0",
            "commodity": commodity,
            "flow": flow or "",
            "period": period or "now",
        }

        def _fetch():
            params = {
                "type": "C",
                "freq": freq,
                "px": "HS",
                "ps": period or "now",
                "r": reporter or "all",
                "p": partner or "0",
                "cc": commodity,
                "fmt": "json",
            }
            if flow:
                params["rg"] = flow
            if self.api_key:
                params["apikey"] = self.api_key

            url = f"{V2_BASE}/get"
            resp = httpx.get(url, params=params, timeout=60)
            resp.raise_for_status()
            data = resp.json()
            return pd.DataFrame(data.get("data", data.get("dataset", [])))

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
        use_v2: bool = True,
        normalize: bool = True,
    ) -> pd.DataFrame:
        if use_v2:
            return self.get_trade_data_v2(
                freq=freq,
                reporter=origin,
                partner=destination,
                commodity=commodity,
                period=period,
                normalize=normalize,
            )
        else:
            return self.get_trade_data_v1(
                freq=freq,
                reporter=origin,
                partner=destination,
                commodity=commodity,
                period=period,
                normalize=normalize,
            )

    def _to_canonical(self, df: pd.DataFrame) -> pd.DataFrame:
        out = pd.DataFrame()
        period_col = df.get("period", df.get("Period", df.get("yr", pd.NA)))
        if not period_col.isna().all():
            out["date"] = pd.to_datetime(period_col.astype(str), errors="coerce")
        else:
            out["date"] = pd.NaT

        reporter_col = df.get(
            "reporterISO", df.get("ReporterISO", df.get("rtTitle", pd.NA))
        )
        if not reporter_col.isna().all():
            if reporter_col.dtype == object:
                out["origin_iso3"] = reporter_col.str.upper().str[:3]
            else:
                out["origin_iso3"] = reporter_col.astype(str).str.upper().str[:3]

        partner_col = df.get(
            "partnerISO", df.get("PartnerISO", df.get("ptTitle", pd.NA))
        )
        if not partner_col.isna().all():
            if partner_col.dtype == object:
                out["destination_iso3"] = partner_col.str.upper().str[:3]
            else:
                out["destination_iso3"] = partner_col.astype(str).str.upper().str[:3]

        cmd_col = df.get(
            "commodityCode", df.get("CommodityCode", df.get("cmdCode", pd.NA))
        )
        if not cmd_col.isna().all():
            out["commodity_code"] = cmd_col.astype(str)

        value_col = df.get("tradeValue", df.get("TradeValue", df.get("TradeValueInUSD", df.get("tv", pd.NA))))
        if not value_col.isna().all():
            out["value"] = pd.to_numeric(value_col, errors="coerce")

        out["source"] = "UN Comtrade"
        return out.dropna(subset=["value"])
