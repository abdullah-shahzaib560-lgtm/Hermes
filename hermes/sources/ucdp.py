import json
import logging
from datetime import timedelta
from typing import Optional

import pandas as pd
import urllib.request

from hermes.core.cache import RawCache

logger = logging.getLogger(__name__)

API_BASE = "https://ucdpapi.uu.se/api/v1"

COUNTRY_MAP = {
    "Ukraine": "UKR", "Ukraine ": "UKR", "ukraine": "UKR",
    "Russia": "RUS", "Russian Federation": "RUS",
    "United States": "USA", "United States of America": "USA",
    "China": "CHN", "India": "IND", "Brazil": "BRA",
    "United Kingdom": "GBR", "France": "FRA", "Germany": "DEU",
    "Japan": "JPN", "Canada": "CAN", "Australia": "AUS",
    "Italy": "ITA", "Spain": "ESP", "Mexico": "MEX",
    "Indonesia": "IDN", "Turkey": "TUR", "Türkiye": "TUR",
    "Korea": "KOR", "South Korea": "KOR",
    "Saudi Arabia": "SAU", "Iran": "IRN", "Iraq": "IRQ",
    "Israel": "ISR", "Pakistan": "PAK", "Egypt": "EGY",
    "Nigeria": "NGA", "South Africa": "ZAF", "Argentina": "ARG",
    "Colombia": "COL", "Chile": "CHL", "Peru": "PER",
    "Venezuela": "VEN", "Thailand": "THA", "Viet Nam": "VNM",
    "Vietnam": "VNM", "Malaysia": "MYS", "Philippines": "PHL",
    "Poland": "POL", "Netherlands": "NLD", "Sweden": "SWE",
    "Norway": "NOR", "Denmark": "DNK", "Finland": "FIN",
    "Belgium": "BEL", "Austria": "AUT", "Switzerland": "CHE",
    "Greece": "GRC", "Portugal": "PRT", "Czech Republic": "CZE",
    "Hungary": "HUN", "Romania": "ROU", "Ukraine": "UKR",
    "Belarus": "BLR", "Kazakhstan": "KAZ",
    "Syria": "SYR", "Yemen": "YEM", "Libya": "LBY",
    "Sudan": "SDN", "South Sudan": "SSD",
    "Dem. Rep. of the Congo": "COD", "DR Congo": "COD",
    "Ethiopia": "ETH", "Somalia": "SOM", "Afghanistan": "AFG",
    "Myanmar": "MMR", "Mali": "MLI", "Central African Republic": "CAF",
}


def _map_country(name: str) -> str:
    cleaned = name.strip() if name else ""
    if not cleaned:
        return cleaned
    return COUNTRY_MAP.get(cleaned, cleaned.upper()[:3])


class UCDP:
    def __init__(self, cache: RawCache | None = None):
        self._cache = cache

    def _fetch_json(self, url: str) -> dict:
        req = urllib.request.Request(url, headers={
            "User-Agent": "Hermes/0.1", "Accept": "application/json",
        })
        with urllib.request.urlopen(req, timeout=60) as resp:
            return json.loads(resp.read().decode())

    def _cached(self, params: dict, fetch_fn, force: bool = False):
        if self._cache is None:
            return fetch_fn()
        return self._cache.get_or_fetch("ucdp", params, fetch_fn, force=force, ttl=timedelta(hours=24))

    def get_ged_events(
        self,
        country: Optional[str] = None,
        year_from: Optional[int] = None,
        year_to: Optional[int] = None,
        max_records: int = 10000,
        normalize: bool = True,
        force: bool = False,
    ) -> pd.DataFrame:
        cache_params = {
            "q": "get_ged_events", "country": country or "",
            "year_from": year_from or 0, "year_to": year_to or 0, "max": max_records,
        }

        def _fetch():
            params = {"pagesize": min(max_records, 10000), "page": 1}
            if country:
                params["country"] = country
            if year_from:
                params["year_min"] = year_from
            if year_to:
                params["year_max"] = year_to

            all_records = []
            while True:
                qs = "&".join(f"{k}={v}" for k, v in params.items())
                url = f"{API_BASE}/ged/events?{qs}"
                data = self._fetch_json(url)
                results = data.get("Result", data.get("results", data.get("data", [])))
                if not results:
                    break
                all_records.extend(results)
                total = data.get("TotalPages", data.get("totalPages", 1))
                if params["page"] >= total:
                    break
                params["page"] += 1
            return pd.DataFrame(all_records)

        df = self._cached(cache_params, _fetch, force=force)
        if df.empty:
            return df
        return self._to_ged_canonical(df) if normalize else df

    def get_battle_related_deaths(
        self,
        country: Optional[str] = None,
        year_from: Optional[int] = None,
        year_to: Optional[int] = None,
        normalize: bool = True,
        force: bool = False,
    ) -> pd.DataFrame:
        cache_params = {
            "q": "get_brd", "country": country or "",
            "year_from": year_from or 0, "year_to": year_to or 0,
        }

        def _fetch():
            params = {}
            if country:
                params["country"] = country
            if year_from:
                params["year_min"] = year_from
            if year_to:
                params["year_max"] = year_to
            qs = "&".join(f"{k}={v}" for k, v in params.items()) if params else ""
            url = f"{API_BASE}/brd/deaths?{qs}" if qs else f"{API_BASE}/brd/deaths"
            data = self._fetch_json(url)
            return pd.DataFrame(data.get("Result", data.get("results", data.get("data", []))))

        df = self._cached(cache_params, _fetch, force=force)
        if df.empty:
            return df
        return self._to_brd_canonical(df) if normalize else df

    def _to_ged_canonical(self, df: pd.DataFrame) -> pd.DataFrame:
        if df.empty:
            return df
        out = pd.DataFrame()

        id_col = next((c for c in ["id", "Id", "event_id", "EventId"] if c in df.columns), None)
        if id_col:
            out["event_id"] = df[id_col].astype(str)

        date_col = next((c for c in ["date_start", "DateStart", "date_end", "Date"] if c in df.columns), None)
        if date_col:
            out["date"] = pd.to_datetime(df[date_col], errors="coerce")

        country_col = next((c for c in ["country", "Country", "location"] if c in df.columns), None)
        if country_col:
            out["country_iso3"] = df[country_col].astype(str).apply(_map_country)

        type_col = next((c for c in ["type_of_violence", "TypeOfViolence", "event_type"] if c in df.columns), None)
        if type_col:
            out["event_type"] = df[type_col].astype(str)
        else:
            out["event_type"] = "armed_conflict"

        sev_col = next((c for c in ["best", "Best", "deaths_civilians", "high", "low", "severity"] if c in df.columns), None)
        if sev_col:
            out["severity"] = pd.to_numeric(df[sev_col], errors="coerce")

        lat_col = next((c for c in ["latitude", "Latitude"] if c in df.columns), None)
        if lat_col:
            out["lat"] = pd.to_numeric(df[lat_col], errors="coerce")

        lon_col = next((c for c in ["longitude", "Longitude"] if c in df.columns), None)
        if lon_col:
            out["lon"] = pd.to_numeric(df[lon_col], errors="coerce")

        out["source"] = "UCDP GED"
        cols = ["event_id", "date", "country_iso3", "event_type", "severity", "lat", "lon", "source"]
        for col in cols:
            if col not in out.columns:
                out[col] = None
        return out.dropna(subset=["event_id"]).reset_index(drop=True)

    def _to_brd_canonical(self, df: pd.DataFrame) -> pd.DataFrame:
        if df.empty:
            return df
        out = pd.DataFrame()

        id_col = next((c for c in ["id", "Id", "conflict_id"] if c in df.columns), None)
        if id_col:
            out["event_id"] = df[id_col].astype(str)

        year_col = next((c for c in ["year", "Year"] if c in df.columns), None)
        if year_col:
            out["date"] = pd.to_datetime(df[year_col].astype(str) + "-01-01", errors="coerce")

        country_col = next((c for c in ["country", "Country", "location"] if c in df.columns), None)
        if country_col:
            out["country_iso3"] = df[country_col].astype(str).apply(_map_country)

        out["event_type"] = "battle_related_death"

        sev_col = next((c for c in ["best_estimate", "BestEstimate", "best", "deaths", "Deaths", "low", "high", "severity"] if c in df.columns), None)
        if sev_col:
            out["severity"] = pd.to_numeric(df[sev_col], errors="coerce")

        out["lat"] = None
        out["lon"] = None
        out["source"] = "UCDP BRD"
        cols = ["event_id", "date", "country_iso3", "event_type", "severity", "lat", "lon", "source"]
        for col in cols:
            if col not in out.columns:
                out[col] = None
        return out.dropna(subset=["event_id"]).reset_index(drop=True)
