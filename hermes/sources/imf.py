import logging
import xml.etree.ElementTree as ET
from datetime import timedelta
from typing import Optional

import pandas as pd
import urllib.request

from hermes.core.cache import RawCache

logger = logging.getLogger(__name__)

BASE = "https://api.imf.org/external/sdmx/2.1"

COUNTRY_IMF = {
    "USA": "U019", "CHN": "U142", "JPN": "U150", "DEU": "U134", "FRA": "U132",
    "GBR": "U112", "ITA": "U136", "CAN": "U156", "AUS": "U193", "KOR": "U542",
    "RUS": "U922", "BRA": "U223", "IND": "U534", "MEX": "U273", "IDN": "U536",
    "TUR": "U186", "SAU": "U456", "ZAF": "U199", "ARG": "U213", "UKR": "U926",
    "CHE": "U146", "NLD": "U138", "ESP": "U184", "SWE": "U144", "NOR": "U142",
    "POL": "U964", "BEL": "U124", "AUT": "U122", "DNK": "U128", "FIN": "U172",
    "PRT": "U182", "GRC": "U174", "IRL": "U176", "CZE": "U935", "HUN": "U944",
    "ROU": "U968", "CHL": "U228", "COL": "U233", "PER": "U293", "EGY": "U469",
    "NGA": "U694", "KEN": "U664", "MAR": "U686", "TUN": "U744", "DZA": "U612",
    "ARE": "U466", "QAT": "U453", "KWT": "U443", "IRN": "U429", "IRQ": "U433",
    "ISR": "U436", "PAK": "U564", "BGD": "U513", "PHL": "U566", "THA": "U578",
    "MYS": "U548", "SGP": "U576", "VNM": "U582", "HKG": "U532", "TWN": "U528",
    "NZL": "U196", "ZWE": "U698", "AGO": "U614", "ETH": "U644", "GHA": "U652",
    "SDN": "U732", "LBY": "U672", "YEM": "U791", "OMN": "U449", "BHR": "U419",
    "JOR": "U439", "LBN": "U446", "KAZ": "U916", "AZE": "U915", "BLR": "U913",
    "UKR": "U926", "UGA": "U746", "TZA": "U738", "CMR": "U622", "CIV": "U662",
    "GIN": "U656", "SEN": "U722", "BFA": "U748", "MWI": "U676", "RWA": "U714",
    "ZMB": "U754", "MOZ": "U688", "MDG": "U674", "TCD": "U628", "NER": "U692",
    "BEN": "U638", "SLE": "U724", "TGO": "U742", "CAF": "U626", "LSO": "U668",
    "ERI": "U643", "BDI": "U618", "DJI": "U640", "MRT": "U682", "GMB": "U648",
    "GNB": "U654", "SWZ": "U734", "COM": "U632", "MUS": "U684", "SYC": "U716",
    "CPV": "U624", "STP": "U728",
}

_REV_IMF = {v: k for k, v in COUNTRY_IMF.items()}
_IMF_GROUPS = {"G001": "World", "G110": "Advanced", "G119": "EuroArea", "G120": "EMDE"}

INDICATOR_MAP = {
    "NGDP_XDC": ("B1GQ_S1_V", "SA_PU", "9"),
    "NGDP_R_XDC": ("B1GQ_S1_Q", "IX", "0"),
    "NGDP_XDC_Q": ("B1GQ_S1_Q", "SA_PU", "9"),
    "PCPI_IX": ("PCPI_IX", None, None),
    "AIP_IX": ("AIP_IX", None, None),
}

FALLBACK_MAP = {
    "BCA_BP6_USD": ("BOP", "CAB"),
    "FMA_RESM_USD": ("BOP", "RESFL"),
    "BM_GS_GNFS_CD": ("BOP", "BM"),
}

FLOWS = {
    "IFS": {"id": "QGDP_WCA"},
    "BOP": {"id": "BOP"},
    "CPI": {"id": "CPI"},
    "PPI": {"id": "PPI"},
    "WEO": {"id": "WEO"},
    "FAS": {"id": "FAS"},
    "FDI": {"id": "FDI"},
    "NSDP": {"id": "NSDP"},
}


class IMF:
    _all_caches: dict[str, pd.DataFrame] = {}

    def __init__(self, cache: RawCache | None = None):
        self._cache = cache

    def _fetch(self, url: str) -> bytes:
        req = urllib.request.Request(url, headers={"User-Agent": "Hermes/0.1"})
        with urllib.request.urlopen(req, timeout=60) as resp:
            return resp.read()

    def _cached(self, params: dict, fetch_fn, force: bool = False):
        if self._cache is None:
            return fetch_fn()
        return self._cache.get_or_fetch("imf", params, fetch_fn, force=force, ttl=timedelta(hours=24))

    def _fetch_dataflow(self, flow_key: str, force: bool = False) -> pd.DataFrame:
        if flow_key in self._all_caches and not force:
            return self._all_caches[flow_key]
        flow = FLOWS.get(flow_key)
        if flow is None:
            return pd.DataFrame()
        raw = self._fetch(f"{BASE}/data/{flow['id']}/all")
        df = self._parse_xml(raw)
        self._all_caches[flow_key] = df
        return df

    def _fetch_dataflow_for(self, flow_key: str, country_iso3: str | None, start_period: str | None = None, end_period: str | None = None, force: bool = False) -> pd.DataFrame:
        if flow_key == "IFS":
            imf_code = COUNTRY_IMF.get(country_iso3.upper()) if country_iso3 else None
            param = imf_code if imf_code else "all"
        else:
            param = country_iso3 if country_iso3 else "all"
        cache_key = f"{flow_key}/{param}"
        if not force and cache_key in self._all_caches:
            return self._all_caches[cache_key]
        flow = FLOWS.get(flow_key)
        if flow is None:
            return pd.DataFrame()
        url = f"{BASE}/data/{flow['id']}/{param}"
        if flow_key != "IFS":
            qs = []
            if start_period:
                qs.append(f"startPeriod={start_period}")
            if end_period:
                qs.append(f"endPeriod={end_period}")
            qs.append("firstNObservations=10")
            if qs:
                url += "?" + "&".join(qs)
        req = urllib.request.Request(url, headers={"User-Agent": "Hermes/0.1"})
        with urllib.request.urlopen(req, timeout=300) as resp:
            raw = resp.read()
        df = self._parse_xml(raw)
        self._all_caches[cache_key] = df
        return df

    def _fetch_all(self, force: bool = False) -> pd.DataFrame:
        return self._fetch_dataflow("IFS", force=force)

    def _filter_df(self, df, indicator, country, start_period, end_period, country_col_name: str = "COUNTRY"):
        if country and country.upper() != "ALL" and country_col_name in df.columns:
            vals = df[country_col_name].astype(str)
            iso3 = country.upper()
            imf_code = COUNTRY_IMF.get(iso3)
            if imf_code:
                mask = (vals == iso3) | (vals == imf_code)
                df = df[mask]

        if indicator and indicator.upper() != "ALL" and "INDICATOR" in df.columns:
            ind_info = INDICATOR_MAP.get(indicator)
            if ind_info:
                ind_code = ind_info[0]
                df = df[df["INDICATOR"] == ind_code]
                if len(ind_info) > 1 and ind_info[1] and "TYPE_OF_TRANSFORMATION" in df.columns:
                    df = df[df["TYPE_OF_TRANSFORMATION"] == ind_info[1]]
                if len(ind_info) > 2 and ind_info[2] and "SCALE" in df.columns:
                    df = df[df["SCALE"] == str(ind_info[2])]
            else:
                df = df[df["INDICATOR"] == indicator]

        if start_period and "TIME_PERIOD" in df.columns:
            df = df[df["TIME_PERIOD"].astype(str) >= start_period]
        if end_period and "TIME_PERIOD" in df.columns:
            df = df[df["TIME_PERIOD"].astype(str) <= end_period]
        return df

    def get_data(
        self,
        indicator: str = "NGDP_XDC",
        country: str = "",
        freq: str = "A",
        start_period: Optional[str] = None,
        end_period: Optional[str] = None,
        database: str = "IFS",
        normalize: bool = True,
        force: bool = False,
    ) -> pd.DataFrame:
        cache_params = {
            "q": "get_data", "indicator": indicator,
            "country": country or "", "freq": freq,
            "start": start_period or "", "end": end_period or "",
            "database": database,
        }

        def _fetch():
            df = self._fetch_dataflow(database, force=force)
            if df.empty:
                return df
            df = self._filter_df(df, indicator, country, start_period, end_period)
            if not df.empty:
                return df.reset_index(drop=True)

            fallback = FALLBACK_MAP.get(indicator)
            if fallback is not None:
                fb_db, fb_ind = fallback
                fb_iso3 = country.upper() if country and country.upper() != "ALL" else None
                fb_df = self._fetch_dataflow_for(fb_db, fb_iso3, start_period=start_period, end_period=end_period, force=force)
                if not fb_df.empty:
                    fb_df = self._filter_df(fb_df, fb_ind, country, start_period, end_period)
                    if not fb_df.empty:
                        return fb_df.reset_index(drop=True)
            return pd.DataFrame()

        self._last_indicator = indicator
        df = self._cached(cache_params, _fetch, force=force)
        if df.empty:
            return df
        return self._to_canonical(df) if normalize else df

    def list_countries(self) -> pd.DataFrame:
        df = self._fetch_all()
        if df.empty or "INDICATOR" not in df.columns:
            return pd.DataFrame()
        gdp = df[df["INDICATOR"] == "B1GQ_S1_V"].copy()
        if gdp.empty or "COUNTRY" not in gdp.columns or "TIME_PERIOD" not in gdp.columns:
            return pd.DataFrame()
        lv = gdp.loc[gdp.groupby("COUNTRY")["TIME_PERIOD"].idxmax()].copy()
        lv["value"] = pd.to_numeric(lv.get("OBS_VALUE", pd.Series(dtype=float)), errors="coerce")
        lv["country_iso3"] = lv["COUNTRY"].map(_REV_IMF)
        return lv[["country_iso3", "value", "TIME_PERIOD"]].dropna(subset=["country_iso3"]).sort_values("country_iso3").reset_index(drop=True)

    def list_indicators(self, database: str = "IFS") -> list[str]:
        df = self._fetch_dataflow(database)
        if df.empty or "INDICATOR" not in df.columns:
            return []
        return sorted(df["INDICATOR"].unique())

    def _parse_xml(self, raw: bytes) -> pd.DataFrame:
        rows = []
        tree = ET.fromstring(raw)
        for series in tree.iter("*"):
            tag = series.tag.split("}")[-1] if "}" in series.tag else series.tag
            if tag != "Series":
                continue
            row = dict(series.attrib)
            for obs in series.iter("*"):
                otag = obs.tag.split("}")[-1] if "}" in obs.tag else obs.tag
                if otag != "Obs":
                    continue
                r = dict(row)
                r.update(obs.attrib)
                rows.append(r)
        return pd.DataFrame(rows)

    def _to_canonical(self, df: pd.DataFrame) -> pd.DataFrame:
        if df.empty:
            return df
        col = next((c for c in df.columns if c in ("COUNTRY", "REF_AREA")), None)
        ind_col = next((c for c in df.columns if c in ("INDICATOR", "SERIES_NAME")), None)
        val_col = next((c for c in df.columns if c in ("OBS_VALUE", "VALUE")), None)
        time_col = next((c for c in df.columns if c in ("TIME_PERIOD", "PERIOD")), None)

        out = pd.DataFrame()
        if time_col:
            raw = df[time_col].astype(str).str[:10]
            out["date"] = pd.to_datetime(raw, errors="coerce")

        if col:
            codes = df[col].astype(str)
            mapped = codes.map(_REV_IMF)
            out["country_iso3"] = mapped.where(mapped.notna(), codes)

        out["indicator_id"] = getattr(self, "_last_indicator", df.get(ind_col, "") if ind_col else "")

        if val_col:
            out["value"] = pd.to_numeric(df[val_col], errors="coerce")

        out["source"] = "IMF"
        for c in ["date", "country_iso3", "indicator_id", "value"]:
            if c not in out.columns:
                out[c] = None
        return out.dropna(subset=["date", "country_iso3", "indicator_id", "value"]).reset_index(drop=True)
