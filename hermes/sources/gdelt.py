import io
import zipfile
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta
from typing import Literal
from urllib.parse import urlencode

import httpx
import pandas as pd

from hermes.core.cache import RawCache

logger = logging.getLogger(__name__)

CANONICAL_COLUMNS = [
    "event_id", "date", "country_iso3", "event_type",
    "severity", "lat", "lon", "source",
]

CAMEO_EVENT_TYPES: dict[int, str] = {
    0: "statement",
    1: "yield",
    2: "comment",
    3: "consult",
    4: "diplomatic_cooperation",
    5: "material_cooperation",
    6: "provide_aid",
    7: "grant_asylum",
    8: "endorse",
    9: "agree",
    10: "demand",
    11: "disapprove",
    12: "reject",
    13: "threaten",
    14: "protest",
    15: "display_force",
    16: "reduce_relations",
    17: "sanction",
    18: "assault",
    19: "fight",
    20: "mass_violence",
}

EVENT_THEMES: dict[str, list[int]] = {
    "ALL_COOPERATION": list(range(0, 10)),
    "ALL_CONFLICT": list(range(10, 21)),
    "PROTEST": [14],
    "CONFLICT": [18, 19, 20],
    "DIPLOMACY": [4, 5, 6, 7, 8, 9],
    "SANCTIONS": [17],
    "ASSAULT": [18],
    "FIGHT": [19],
    "MASS_VIOLENCE": [20],
}

FIPS_TO_ISO3: dict[str, str] = {
    "AF": "AFG", "AL": "ALB", "AG": "DZA", "AN": "AND", "AO": "AGO",
    "AC": "ATG", "AR": "ARG", "AM": "ARM", "AS": "AUS", "AU": "AUT",
    "AJ": "AZE", "BF": "BHS", "BA": "BHR", "BG": "BGD", "BB": "BRB",
    "BO": "BLR", "BE": "BEL", "BH": "BLZ", "BN": "BEN", "BT": "BTN",
    "BL": "BOL", "BK": "BIH", "BC": "BWA", "BR": "BRA", "BX": "BRN",
    "BU": "BGR", "UV": "BFA", "BM": "MMR", "BY": "BDI", "CB": "KHM",
    "CM": "CMR", "CA": "CAN", "CV": "CPV", "CT": "CAF", "CD": "TCD",
    "CI": "CHL", "CH": "CHN", "CO": "COL", "CN": "COM", "CF": "COG",
    "CG": "COD", "CS": "CRI", "IV": "CIV", "HR": "HRV", "CU": "CUB",
    "CY": "CYP", "EZ": "CZE", "DA": "DNK", "DJ": "DJI", "DO": "DMA",
    "DR": "DOM", "EC": "ECU", "EG": "EGY", "ES": "SLV", "EK": "GNQ",
    "ER": "ERI", "EN": "EST", "ET": "ETH", "FJ": "FJI", "FI": "FIN",
    "FR": "FRA", "GB": "GAB", "GA": "GMB", "GG": "GEO", "GM": "DEU",
    "GH": "GHA", "GR": "GRC", "GJ": "GRD", "GT": "GTM", "GV": "GIN",
    "PU": "GNB", "GY": "GUY", "HA": "HTI", "HO": "HND", "HU": "HUN",
    "IC": "ISL", "IN": "IND", "ID": "IDN", "IR": "IRN", "IZ": "IRQ",
    "EI": "IRL", "IS": "ISR", "IT": "ITA", "JM": "JAM", "JA": "JPN",
    "JO": "JOR", "KZ": "KAZ", "KE": "KEN", "KR": "KIR", "KS": "KOR",
    "KV": "XKX", "KU": "KWT", "KG": "KGZ", "LA": "LAO", "LG": "LVA",
    "LE": "LBN", "LT": "LSO", "LI": "LBR", "LY": "LBY", "LS": "LIE",
    "LH": "LTU", "LU": "LUX", "MK": "MKD", "MA": "MDG", "MI": "MWI",
    "MY": "MYS", "MV": "MDV", "ML": "MLI", "MT": "MLT", "RM": "MHL",
    "MR": "MRT", "MP": "MUS", "MX": "MEX", "FM": "FSM", "MD": "MDA",
    "MN": "MNG", "MJ": "MNE", "MO": "MAR", "MZ": "MOZ", "WA": "NAM",
    "NR": "NRU", "NP": "NPL", "NL": "NLD", "NZ": "NZL", "NU": "NIC",
    "NG": "NER", "NI": "NGA", "NO": "NOR", "MU": "OMN", "PK": "PAK",
    "PW": "PLW", "PM": "PAN", "PP": "PNG", "PA": "PRY", "PE": "PER",
    "RP": "PHL", "PL": "POL", "PO": "PRT", "QA": "QAT", "RO": "ROU",
    "RS": "RUS", "RW": "RWA", "SC": "KNA", "ST": "LCA", "VC": "VCT",
    "WS": "WSM", "SM": "SMR", "TP": "STP", "SA": "SAU", "SG": "SEN",
    "RI": "SRB", "SE": "SYC", "SL": "SLE", "SN": "SGP", "LO": "SVK",
    "SI": "SVN", "BP": "SLB", "SO": "SOM", "SF": "ZAF", "OD": "SSD",
    "SP": "ESP", "CE": "LKA", "SU": "SDN", "NS": "SUR", "WZ": "SWZ",
    "SW": "SWE", "SZ": "CHE", "SY": "SYR", "TI": "TJK", "TZ": "TZA",
    "TH": "THA", "TT": "TLS", "TO": "TGO", "TN": "TON", "TD": "TTO",
    "TS": "TUN", "TU": "TUR", "TX": "TKM", "TV": "TUV", "UG": "UGA",
    "UP": "UKR", "AE": "ARE", "UK": "GBR", "US": "USA", "UY": "URY",
    "UZ": "UZB", "NH": "VUT", "VT": "VAT", "VE": "VEN", "VM": "VNM",
    "YM": "YEM", "ZA": "ZMB", "ZI": "ZWE",
}

ISO3_TO_FIPS = {v: k for k, v in FIPS_TO_ISO3.items()}

GDELT_EVENT_COLUMNS = [
    "GlobalEventID", "SQLDATE", "MonthYear", "Year", "FractionDate",
    "Actor1Code", "Actor1Name", "Actor1CountryCode", "Actor1KnownGroupCode",
    "Actor1EthnicCode", "Actor1Religion1Code", "Actor1Religion2Code",
    "Actor1Type1Code", "Actor1Type2Code", "Actor1Type3Code",
    "Actor2Code", "Actor2Name", "Actor2CountryCode", "Actor2KnownGroupCode",
    "Actor2EthnicCode", "Actor2Religion1Code", "Actor2Religion2Code",
    "Actor2Type1Code", "Actor2Type2Code", "Actor2Type3Code",
    "IsRootEvent", "EventCode", "EventBaseCode", "EventRootCode", "QuadClass",
    "GoldsteinScale", "NumMentions", "NumSources", "NumArticles", "AvgTone",
    "Actor1Geo_Type", "Actor1Geo_FullName", "Actor1Geo_CountryCode",
    "Actor1Geo_ADM1Code", "Actor1Geo_ADM2Code", "Actor1Geo_Lat", "Actor1Geo_Long",
    "Actor1Geo_FeatureID",
    "Actor2Geo_Type", "Actor2Geo_FullName", "Actor2Geo_CountryCode",
    "Actor2Geo_ADM1Code", "Actor2Geo_ADM2Code", "Actor2Geo_Lat", "Actor2Geo_Long",
    "Actor2Geo_FeatureID",
    "ActionGeo_Type", "ActionGeo_FullName", "ActionGeo_CountryCode",
    "ActionGeo_ADM1Code", "ActionGeo_ADM2Code", "ActionGeo_Lat", "ActionGeo_Long",
    "ActionGeo_FeatureID",
    "DATEADDED", "SOURCEURL",
]

GDELT_2_API = "https://api.gdeltproject.org/api/v2/analyze/analyze"
GDELT_MASTER = "http://data.gdeltproject.org/gdeltv2/masterfilelist.txt"


class GDELT:

    def __init__(self, cache: RawCache | None = None):
        self._cache = cache or RawCache()
        self._master_df: pd.DataFrame | None = None


    @staticmethod
    def _to_canonical(df: pd.DataFrame) -> pd.DataFrame:
        if df.empty:
            return pd.DataFrame(columns=CANONICAL_COLUMNS)

        out = pd.DataFrame()

        for c in ("eventid", "GlobalEventID"):
            if c in df.columns:
                out["event_id"] = df[c].astype(str)
                break

        if "date" in df.columns:
            out["date"] = pd.to_datetime(df["date"], errors="coerce")
        elif "SQLDATE" in df.columns:
            out["date"] = pd.to_datetime(df["SQLDATE"], format="%Y%m%d", errors="coerce")

        if "ActionGeo_CountryCode" in df.columns:
            out["country_iso3"] = (
                df["ActionGeo_CountryCode"]
                .map(FIPS_TO_ISO3)
                .fillna(df["ActionGeo_CountryCode"])
            )
        elif "countrycode" in df.columns:
            out["country_iso3"] = (
                df["countrycode"].map(FIPS_TO_ISO3).fillna(df["countrycode"])
            )

        for c in ("EventRootCode", "eventrootcode"):
            if c in df.columns:
                root = pd.to_numeric(df[c], errors="coerce").fillna(-1).astype(int)
                out["event_type"] = root.map(CAMEO_EVENT_TYPES).fillna("unknown")
                break

        for c in ("GoldsteinScale", "goldsteinscale"):
            if c in df.columns:
                out["severity"] = pd.to_numeric(df[c], errors="coerce")
                break

        # lat / lon
        for lat_c, lon_c in (
            ("ActionGeo_Lat", "ActionGeo_Long"),
            ("actiongeolat", "actiongeolong"),
        ):
            if lat_c in df.columns and lon_c in df.columns:
                out["lat"] = pd.to_numeric(df[lat_c], errors="coerce")
                out["lon"] = pd.to_numeric(df[lon_c], errors="coerce")
                break

        out["source"] = "gdelt"
        out = out[[c for c in CANONICAL_COLUMNS if c in out.columns]]
        out = out.dropna(subset=["date"]).reset_index(drop=True)
        return out


    def _fetch_via_api(
        self,
        countries: list[str] | None = None,
        root_codes: list[int] | None = None,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
        timeout: float = 30.0,
        retries: int = 2,
    ) -> pd.DataFrame:
        params: dict = {"mode": "EventList", "format": "json"}

        if countries:
            fips = [ISO3_TO_FIPS.get(c.upper(), c.upper()) for c in countries]
            params["country"] = "|".join(fips)

        if root_codes:
            params["theme"] = "|".join(str(r) for r in sorted(set(root_codes)))

        if start_date:
            params["startdate"] = start_date.strftime("%Y%m%d%H%M%S")
        if end_date:
            params["enddate"] = end_date.strftime("%Y%m%d%H%M%S")

        url = f"{GDELT_2_API}?{urlencode(params, doseq=True)}"
        logger.debug("GDELT Analysis API: %s", url[:250])

        for attempt in range(retries):
            try:
                resp = httpx.get(url, timeout=timeout, follow_redirects=True)
                resp.raise_for_status()
                break
            except httpx.ReadTimeout:
                if attempt == retries - 1:
                    raise
                logger.warning("GDELT API timeout, retry %d", attempt + 1)

        data = resp.json()
        events = data.get("events", data.get("result", []))
        if not events:
            return pd.DataFrame()
        return pd.DataFrame(events)


    def _load_master_list(self, timeout: float = 60.0) -> pd.DataFrame:
        if self._master_df is not None:
            return self._master_df

        resp = httpx.get(GDELT_MASTER, timeout=timeout)
        resp.raise_for_status()

        df = pd.read_csv(
            io.StringIO(resp.text),
            sep=r"\s+",
            header=None,
            names=["size", "hash", "url"],
        )
        df = df[df["url"].str.contains("export.CSV.zip", na=False)].copy()
        df["timestamp"] = pd.to_datetime(
            df["url"].str.extract(r"/(\d{14})\.export")[0],
            format="%Y%m%d%H%M%S",
        )
        df = df.sort_values("timestamp").reset_index(drop=True)
        self._master_df = df
        return df

    def _urls_in_range(self, start: datetime, end: datetime) -> list[str]:
        master = self._load_master_list()
        mask = (master["timestamp"] >= start) & (master["timestamp"] <= end)
        return master.loc[mask, "url"].tolist()

    def _download_one(
        self, url: str, timeout: float = 30.0, retries: int = 3
    ) -> pd.DataFrame:
        for attempt in range(retries):
            try:
                resp = httpx.get(url, timeout=timeout, follow_redirects=True)
                resp.raise_for_status()
                break
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 404:
                    logger.warning("404 for %s", url)
                    return pd.DataFrame(columns=GDELT_EVENT_COLUMNS)
                raise
            except httpx.ReadTimeout:
                if attempt == retries - 1:
                    raise

        with zipfile.ZipFile(io.BytesIO(resp.content)) as zf:
            inner = zf.namelist()[0]
            with zf.open(inner) as f:
                return pd.read_csv(
                    f, sep="\t", header=None, names=GDELT_EVENT_COLUMNS, dtype=str
                )

    def _fetch_via_exports(
        self,
        country_code: str,
        start_date: datetime,
        end_date: datetime,
        root_codes: list[int] | None = None,
        max_workers: int = 8,
        max_files: int = 96,
    ) -> pd.DataFrame:
        urls = self._urls_in_range(start_date, end_date)
        if not urls:
            logger.warning("No GDELT files in range %s – %s", start_date, end_date)
            return pd.DataFrame(columns=GDELT_EVENT_COLUMNS)

        if len(urls) > max_files:
            logger.warning(
                "Range covers %d files — capping to last %d", len(urls), max_files
            )
            urls = urls[-max_files:]

        frames: list[pd.DataFrame] = []
        with ThreadPoolExecutor(max_workers=max_workers) as pool:
            fut_map = {pool.submit(self._download_one, u): u for u in urls}
            for fut in as_completed(fut_map):
                try:
                    df = fut.result()
                    if not df.empty:
                        frames.append(df)
                except Exception:
                    logger.exception("Download failed for %s", fut_map[fut])

        if not frames:
            return pd.DataFrame(columns=GDELT_EVENT_COLUMNS)

        full = pd.concat(frames, ignore_index=True)

        # filter by country (FIPS code)
        fips = ISO3_TO_FIPS.get(country_code.upper(), country_code.upper())
        full = full[full["ActionGeo_CountryCode"] == fips].copy()

        if root_codes:
            rc = pd.to_numeric(full["EventRootCode"], errors="coerce")
            full = full[rc.isin(root_codes)].copy()

        numeric_cols = [
            "GoldsteinScale", "NumMentions", "NumSources", "NumArticles", "AvgTone"
        ]
        for col in numeric_cols:
            full[col] = pd.to_numeric(full[col], errors="coerce")

        full["SQLDATE"] = pd.to_datetime(full["SQLDATE"], format="%Y%m%d")
        return full.sort_values("SQLDATE", ascending=False).reset_index(drop=True)


    def query_events(
        self,
        countries: list[str] | None = None,
        themes: list[str] | None = None,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
        normalize: bool = True,
        force: bool = False,
    ) -> pd.DataFrame:

        if themes:
            root_codes: set[int] = set()
            for t in themes:
                t_upper = t.upper()
                if t_upper in EVENT_THEMES:
                    root_codes.update(EVENT_THEMES[t_upper])
                else:
                    try:
                        root_codes.add(int(t))
                    except ValueError:
                        logger.warning("Unknown GDELT theme '%s' — ignoring", t)
            root_codes_list = sorted(root_codes) if root_codes else None
        else:
            root_codes_list = None

        cache_params = {
            "countries": sorted(countries) if countries else [],
            "root_codes": root_codes_list or [],
            "start_date": start_date.isoformat() if start_date else "",
            "end_date": end_date.isoformat() if end_date else "",
        }

        df = self._cache.get_or_fetch(
            source="gdelt",
            params=cache_params,
            fetch_fn=lambda: self._fetch_via_api(
                countries=countries,
                root_codes=root_codes_list,
                start_date=start_date,
                end_date=end_date,
            ),
            force=force,
            ttl=timedelta(hours=6),
        )

        if normalize and not df.empty:
            df = self._to_canonical(df)

        return df

    def fetch(
        self,
        country_code: str,
        start_date: datetime,
        end_date: datetime,
        force: bool = False,
    ) -> pd.DataFrame:

        return self.query_events(
            countries=[country_code],
            start_date=start_date,
            end_date=end_date,
            force=force,
        )
