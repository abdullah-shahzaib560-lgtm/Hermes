import io
import logging
import zipfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta
from typing import Any
from urllib.parse import urlencode

import httpx
import pandas as pd

from hermes.core.cache import RawCache

logger = logging.getLogger(__name__)

CANONICAL_COLUMNS = [
    "event_id",
    "date",
    "country_iso3",
    "event_type",
    "severity",
    "lat",
    "lon",
    "source",
]

GKG_EVENT_TYPES: dict[str, str] = {
    "PROTEST": "protest",
    "TAX_FNCACT_Protest": "protest",
    "TAX_FNCACT_Riot": "protest",
    "GENERAL_CRISIS_RIOTPROTEST": "protest",
    "SOC_RIOT": "protest",
    "CONFLICT": "conflict",
    "GENERAL_CONFLICT": "conflict",
    "MAR_EVENT_MILITARY": "conflict",
    "TAX_FNCACT_Assault": "assault",
    "TAX_FNCACT_Fight": "fight",
    "TAX_FNCACT_Threaten": "threaten",
    "TAX_FNCACT_Sanction": "sanction",
    "TAX_FNCACT_Embargo": "sanction",
    "DIPLOMACY": "diplomacy",
    "TAX_FNCACT_Diplomacy": "diplomacy",
    "TAX_FNCACT_Agree": "diplomacy",
    "TAX_FNCACT_Endorse": "diplomacy",
    "TAX_FNCACT_Appeal": "diplomacy",
}

EVENT_THEMES: dict[str, list[str]] = {
    "PROTEST": ["PROTEST", "TAX_FNCACT_Protest", "TAX_FNCACT_Riot", "GENERAL_CRISIS_RIOTPROTEST", "SOC_RIOT"],
    "CONFLICT": ["CONFLICT", "GENERAL_CONFLICT", "MAR_EVENT_MILITARY", "TAX_FNCACT_Assault", "TAX_FNCACT_Fight"],
    "DIPLOMACY": ["DIPLOMACY", "TAX_FNCACT_Diplomacy", "TAX_FNCACT_Agree", "TAX_FNCACT_Endorse"],
    "SANCTIONS": ["TAX_FNCACT_Sanction", "TAX_FNCACT_Embargo"],
    "ASSAULT": ["TAX_FNCACT_Assault"],
    "FIGHT": ["TAX_FNCACT_Fight"],
    "MASS_VIOLENCE": ["TAX_FNCACT_Assault", "TAX_FNCACT_Fight"],
}

COUNTRIES_ISO3 = [
    "AFG",
    "ALB",
    "DZA",
    "AND",
    "AGO",
    "ATG",
    "ARG",
    "ARM",
    "AUS",
    "AUT",
    "AZE",
    "BHS",
    "BHR",
    "BGD",
    "BRB",
    "BLR",
    "BEL",
    "BLZ",
    "BEN",
    "BTN",
    "BOL",
    "BIH",
    "BWA",
    "BRA",
    "BRN",
    "BGR",
    "BFA",
    "MMR",
    "BDI",
    "KHM",
    "CMR",
    "CAN",
    "CPV",
    "CAF",
    "TCD",
    "CHL",
    "CHN",
    "COL",
    "COM",
    "COG",
    "COD",
    "CRI",
    "CIV",
    "HRV",
    "CUB",
    "CYP",
    "CZE",
    "DNK",
    "DJI",
    "DMA",
    "DOM",
    "ECU",
    "EGY",
    "SLV",
    "GNQ",
    "ERI",
    "EST",
    "ETH",
    "FJI",
    "FIN",
    "FRA",
    "GAB",
    "GMB",
    "GEO",
    "DEU",
    "GHA",
    "GRC",
    "GRD",
    "GTM",
    "GIN",
    "GNB",
    "GUY",
    "HTI",
    "HND",
    "HUN",
    "ISL",
    "IND",
    "IDN",
    "IRN",
    "IRQ",
    "IRL",
    "ISR",
    "ITA",
    "JAM",
    "JPN",
    "JOR",
    "KAZ",
    "KEN",
    "KIR",
    "KOR",
    "XKX",
    "KWT",
    "KGZ",
    "LAO",
    "LVA",
    "LBN",
    "LSO",
    "LBR",
    "LBY",
    "LIE",
    "LTU",
    "LUX",
    "MKD",
    "MDG",
    "MWI",
    "MYS",
    "MDV",
    "MLI",
    "MLT",
    "MHL",
    "MRT",
    "MUS",
    "MEX",
    "FSM",
    "MDA",
    "MNG",
    "MNE",
    "MAR",
    "MOZ",
    "NAM",
    "NRU",
    "NPL",
    "NLD",
    "NZL",
    "NIC",
    "NER",
    "NGA",
    "NOR",
    "OMN",
    "PAK",
    "PLW",
    "PAN",
    "PNG",
    "PRY",
    "PER",
    "PHL",
    "POL",
    "PRT",
    "QAT",
    "ROU",
    "RUS",
    "RWA",
    "KNA",
    "LCA",
    "VCT",
    "WSM",
    "SMR",
    "STP",
    "SAU",
    "SEN",
    "SRB",
    "SYC",
    "SLE",
    "SGP",
    "SVK",
    "SVN",
    "SLB",
    "SOM",
    "ZAF",
    "SSD",
    "ESP",
    "LKA",
    "SDN",
    "SUR",
    "SWZ",
    "SWE",
    "CHE",
    "SYR",
    "TJK",
    "TZA",
    "THA",
    "TLS",
    "TGO",
    "TON",
    "TTO",
    "TUN",
    "TUR",
    "TKM",
    "TUV",
    "UGA",
    "UKR",
    "ARE",
    "GBR",
    "USA",
    "URY",
    "UZB",
    "VUT",
    "VAT",
    "VEN",
    "VNM",
    "YEM",
    "ZMB",
    "ZWE",
]
FIPS = [
    "AF",
    "AL",
    "AG",
    "AN",
    "AO",
    "AC",
    "AR",
    "AM",
    "AS",
    "AU",
    "AJ",
    "BF",
    "BA",
    "BG",
    "BB",
    "BO",
    "BE",
    "BH",
    "BN",
    "BT",
    "BL",
    "BK",
    "BC",
    "BR",
    "BX",
    "BU",
    "UV",
    "BM",
    "BY",
    "CB",
    "CM",
    "CA",
    "CV",
    "CT",
    "CD",
    "CI",
    "CH",
    "CO",
    "CN",
    "CF",
    "CG",
    "CS",
    "IV",
    "HR",
    "CU",
    "CY",
    "EZ",
    "DA",
    "DJ",
    "DO",
    "DR",
    "EC",
    "EG",
    "ES",
    "EK",
    "ER",
    "EN",
    "ET",
    "FJ",
    "FI",
    "FR",
    "GB",
    "GA",
    "GG",
    "GM",
    "GH",
    "GR",
    "GJ",
    "GT",
    "GV",
    "PU",
    "GY",
    "HA",
    "HO",
    "HU",
    "IC",
    "IN",
    "ID",
    "IR",
    "IZ",
    "EI",
    "IS",
    "IT",
    "JM",
    "JA",
    "JO",
    "KZ",
    "KE",
    "KR",
    "KS",
    "KV",
    "KU",
    "KG",
    "LA",
    "LG",
    "LE",
    "LT",
    "LI",
    "LY",
    "LS",
    "LH",
    "LU",
    "MK",
    "MA",
    "MI",
    "MY",
    "MV",
    "ML",
    "MT",
    "RM",
    "MR",
    "MP",
    "MX",
    "FM",
    "MD",
    "MN",
    "MJ",
    "MO",
    "MZ",
    "WA",
    "NR",
    "NP",
    "NL",
    "NZ",
    "NU",
    "NG",
    "NI",
    "NO",
    "MU",
    "PK",
    "PW",
    "PM",
    "PP",
    "PA",
    "PE",
    "RP",
    "PL",
    "PO",
    "QA",
    "RO",
    "RS",
    "RW",
    "SC",
    "ST",
    "VC",
    "WS",
    "SM",
    "TP",
    "SA",
    "SG",
    "RI",
    "SE",
    "SL",
    "SN",
    "LO",
    "SI",
    "BP",
    "SO",
    "SF",
    "OD",
    "SP",
    "CE",
    "SU",
    "NS",
    "WZ",
    "SW",
    "SZ",
    "SY",
    "TI",
    "TZ",
    "TH",
    "TT",
    "TO",
    "TN",
    "TD",
    "TS",
    "TU",
    "TX",
    "TV",
    "UG",
    "UP",
    "AE",
    "UK",
    "US",
    "UY",
    "UZ",
    "NH",
    "VT",
    "VE",
    "VM",
    "YM",
    "ZA",
    "ZI",
]
FIPS_TO_ISO3 = dict(zip(FIPS, COUNTRIES_ISO3))
ISO3_TO_FIPS = {v: k for k, v in FIPS_TO_ISO3.items()}

GDELT_EVENT_COLUMNS = [
    "GlobalEventID",
    "SQLDATE",
    "MonthYear",
    "Year",
    "FractionDate",
    "Actor1Code",
    "Actor1Name",
    "Actor1CountryCode",
    "Actor1KnownGroupCode",
    "Actor1EthnicCode",
    "Actor1Religion1Code",
    "Actor1Religion2Code",
    "Actor1Type1Code",
    "Actor1Type2Code",
    "Actor1Type3Code",
    "Actor2Code",
    "Actor2Name",
    "Actor2CountryCode",
    "Actor2KnownGroupCode",
    "Actor2EthnicCode",
    "Actor2Religion1Code",
    "Actor2Religion2Code",
    "Actor2Type1Code",
    "Actor2Type2Code",
    "Actor2Type3Code",
    "IsRootEvent",
    "EventCode",
    "EventBaseCode",
    "EventRootCode",
    "QuadClass",
    "GoldsteinScale",
    "NumMentions",
    "NumSources",
    "NumArticles",
    "AvgTone",
    "Actor1Geo_Type",
    "Actor1Geo_FullName",
    "Actor1Geo_CountryCode",
    "Actor1Geo_ADM1Code",
    "Actor1Geo_ADM2Code",
    "Actor1Geo_Lat",
    "Actor1Geo_Long",
    "Actor1Geo_FeatureID",
    "Actor2Geo_Type",
    "Actor2Geo_FullName",
    "Actor2Geo_CountryCode",
    "Actor2Geo_ADM1Code",
    "Actor2Geo_ADM2Code",
    "Actor2Geo_Lat",
    "Actor2Geo_Long",
    "Actor2Geo_FeatureID",
    "ActionGeo_Type",
    "ActionGeo_FullName",
    "ActionGeo_CountryCode",
    "ActionGeo_ADM1Code",
    "ActionGeo_ADM2Code",
    "ActionGeo_Lat",
    "ActionGeo_Long",
    "ActionGeo_FeatureID",
    "DATEADDED",
    "SOURCEURL",
]

GDELT_DOC_API = "https://api.gdeltproject.org/api/v2/doc/doc"
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

        for c in ("url", "GlobalEventID", "articleid"):
            if c in df.columns:
                out["event_id"] = df[c].astype(str)
                break

        if "event_id" not in out.columns:
            for c in ("title", "SOURCEURL"):
                if c in df.columns:
                    out["event_id"] = df[c].apply(lambda x: str(hash(str(x)) % 10**12))
                    break

        if "date" in df.columns:
            out["date"] = pd.to_datetime(df["date"], errors="coerce")
        elif "seendate" in df.columns:
            out["date"] = pd.to_datetime(df["seendate"].str[:14], format="%Y%m%d%H%M%S", errors="coerce")
        elif "SQLDATE" in df.columns:
            out["date"] = pd.to_datetime(df["SQLDATE"], format="%Y%m%d", errors="coerce")

        if "ActionGeo_CountryCode" in df.columns:
            out["country_iso3"] = df["ActionGeo_CountryCode"].map(FIPS_TO_ISO3).fillna(df["ActionGeo_CountryCode"])
        elif "sourcecountry" in df.columns:
            out["country_iso3"] = df["sourcecountry"].map(FIPS_TO_ISO3).fillna(df["sourcecountry"])

        if "themes" in df.columns:
            out["event_type"] = df["themes"].apply(_classify_themes)
        elif "EventRootCode" in df.columns:
            _CAMEO = {
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
            rc = pd.to_numeric(df["EventRootCode"], errors="coerce").fillna(-1).astype(int)
            out["event_type"] = rc.map(_CAMEO).fillna("unknown")

        for c in ("tone", "GoldsteinScale", "goldsteinscale"):
            if c in df.columns:
                out["severity"] = pd.to_numeric(df[c], errors="coerce")
                break

        for lat_c, lon_c in (
            ("ActionGeo_Lat", "ActionGeo_Long"),
            ("actiongeolat", "actiongeolong"),
            ("lat", "lon"),
        ):
            if lat_c in df.columns and lon_c in df.columns:
                out["lat"] = pd.to_numeric(df[lat_c], errors="coerce")
                out["lon"] = pd.to_numeric(df[lon_c], errors="coerce")
                break

        out["source"] = "gdelt"
        out = out[[c for c in CANONICAL_COLUMNS if c in out.columns]]
        out = out.dropna(subset=["date"]).reset_index(drop=True)
        return out

    def _fetch_via_doc_api(
        self,
        countries: list[str] | None = None,
        themes: list[str] | None = None,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
        timeout: float = 30.0,
        retries: int = 2,
    ) -> pd.DataFrame:
        query_parts: list[str] = []

        if themes:
            theme_terms = [f"theme:{t}" for t in themes]
            query_parts.append(f"({' OR '.join(theme_terms)})")

        if countries:
            fips = [ISO3_TO_FIPS.get(c.upper(), c.upper()) for c in countries]
            country_terms = [f"sourcecountry:{f}" for f in fips]
            query_parts.append(f"({' OR '.join(country_terms)})")

        query = " ".join(query_parts) if query_parts else " "

        params: dict[str, Any] = {
            "query": query,
            "mode": "artlist",
            "format": "json",
            "maxrecords": 250,
        }

        url = f"{GDELT_DOC_API}?{urlencode(params, doseq=True)}"
        logger.debug("GDELT Doc API: %s", url[:300])

        for attempt in range(retries):
            try:
                resp = httpx.get(url, timeout=timeout, follow_redirects=True)
                resp.raise_for_status()
                break
            except httpx.ReadTimeout:
                if attempt == retries - 1:
                    raise
                logger.warning("GDELT Doc API timeout, retry %d", attempt + 1)

        data = resp.json()
        articles = data.get("articles", data.get("result", []))
        if not articles:
            logger.info("GDELT Doc API returned 0 articles for: %s", query[:200])
            return pd.DataFrame()

        df = pd.DataFrame(articles)
        logger.info("GDELT Doc API returned %d articles", len(df))
        return df

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

    def _download_one(self, url: str, timeout: float = 30.0, retries: int = 3) -> pd.DataFrame:
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
                return pd.read_csv(f, sep="\t", header=None, names=GDELT_EVENT_COLUMNS, dtype=str)

    def _fetch_via_exports(
        self,
        country_code: str,
        start_date: datetime,
        end_date: datetime,
        max_workers: int = 8,
        max_files: int = 96,
    ) -> pd.DataFrame:
        urls = self._urls_in_range(start_date, end_date)
        if not urls:
            logger.warning("No GDELT files in range %s - %s", start_date, end_date)
            return pd.DataFrame(columns=GDELT_EVENT_COLUMNS)
        if len(urls) > max_files:
            logger.warning("Range covers %d files - capping to last %d", len(urls), max_files)
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
        fips = ISO3_TO_FIPS.get(country_code.upper(), country_code.upper())
        full = full[full["ActionGeo_CountryCode"] == fips].copy()

        numeric_cols = ["GoldsteinScale", "NumMentions", "NumSources", "NumArticles", "AvgTone"]
        for c in numeric_cols:
            full[c] = pd.to_numeric(full[c], errors="coerce")
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
            gkg_themes: set[str] = set()
            for t in themes:
                mapped = EVENT_THEMES.get(t.upper(), [t])
                gkg_themes.update(mapped)
        else:
            gkg_themes = set()

        cache_params = {
            "countries": sorted(countries) if countries else [],
            "themes": sorted(gkg_themes) if gkg_themes else [],
            "start_date": start_date.isoformat() if start_date else "",
            "end_date": end_date.isoformat() if end_date else "",
        }

        df = self._cache.get_or_fetch(
            source="gdelt",
            params=cache_params,
            fetch_fn=lambda: self._fetch_via_doc_api(
                countries=countries,
                themes=list(gkg_themes) if gkg_themes else None,
                start_date=start_date,
                end_date=end_date,
            ),
            force=force,
            ttl=timedelta(hours=6),
        )

        if normalize and not df.empty:
            df = self._to_canonical(df)
        return df


def _classify_themes(themes_list: Any) -> str:
    if not isinstance(themes_list, list):
        themes_list = str(themes_list).split(";")
    for t in themes_list:
        t = t.strip()
        label = GKG_EVENT_TYPES.get(t)
        if label:
            return label
    return "unknown"
