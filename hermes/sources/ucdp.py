import pandas as pd
import logging
import urllib.request
import json
from typing import Optional

from hermes.core.cache import RawCache

logger = logging.getLogger(__name__)

API_BASE = "https://ucdpapi.uu.se/api/v1"


class UCDP:
    def __init__(self, cache: RawCache | None = None):
        self._cache = cache

    def _fetch_json(self, url: str) -> dict:
        req = urllib.request.Request(url, headers={"User-Agent": "Hermes/0.1", "Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=60) as resp:
            return json.loads(resp.read().decode())

    def _cached(self, params: dict, fetch_fn, force: bool = False):
        if self._cache is None:
            return fetch_fn()
        return self._cache.get_or_fetch("ucdp", params, fetch_fn, force=force)

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
            "year_from": year_from or 0, "year_to": year_to or 0,
            "max": max_records,
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
        out = pd.DataFrame()
        id_map = {"id": "event_id", "Id": "event_id", "event_id": "event_id", "EventId": "event_id"}
        for src, dst in id_map.items():
            if src in df.columns:
                out[dst] = df[src].astype(str)
                break
        if "event_id" not in out.columns:
            out["event_id"] = None

        date_map = {"date_start": "date", "DateStart": "date", "date_end": "date", "Date": "date"}
        for src in date_map:
            if src in df.columns:
                out["date"] = pd.to_datetime(df[src], errors="coerce")
                break
        if "date" not in out.columns:
            out["date"] = pd.NaT

        country_map = {"country": "country_iso3", "Country": "country_iso3", "location": "country_iso3"}
        for src in country_map:
            if src in df.columns and not df[src].isna().all():
                out["country_iso3"] = df[src].astype(str).str.upper().str[:3]
                break

        type_map = {"type_of_violence": "event_type", "TypeOfViolence": "event_type", "event_type": "event_type"}
        for src in type_map:
            if src in df.columns:
                out["event_type"] = df[src].astype(str)
                break
        if "event_type" not in out.columns:
            out["event_type"] = "armed_conflict"

        sev_map = {"best": "severity", "Best": "severity", "deaths_civilians": "severity", "high": "severity", "low": "severity"}
        for src in sev_map:
            if src in df.columns:
                out["severity"] = pd.to_numeric(df[src], errors="coerce")
                break

        lat_map = {"latitude": "lat", "Latitude": "lat"}
        for src in lat_map:
            if src in df.columns:
                out["lat"] = pd.to_numeric(df[src], errors="coerce")
                break

        lon_map = {"longitude": "lon", "Longitude": "lon"}
        for src in lon_map:
            if src in df.columns:
                out["lon"] = pd.to_numeric(df[src], errors="coerce")
                break

        for col in ["severity", "lat", "lon"]:
            if col not in out.columns:
                out[col] = None

        out["source"] = "UCDP GED"
        return out.dropna(subset=["event_id"])

    def _to_brd_canonical(self, df: pd.DataFrame) -> pd.DataFrame:
        out = pd.DataFrame()
        id_map = {"id": "event_id", "Id": "event_id", "conflict_id": "event_id"}
        for src in id_map:
            if src in df.columns:
                out["event_id"] = df[src].astype(str)
                break
        if "event_id" not in out.columns:
            out["event_id"] = None

        year_map = {"year": "date", "Year": "date"}
        for src in year_map:
            if src in df.columns:
                out["date"] = pd.to_datetime(df[src].astype(str) + "-01-01", errors="coerce")
                break
        if "date" not in out.columns:
            out["date"] = pd.NaT

        country_map = {"country": "country_iso3", "Country": "country_iso3", "location": "country_iso3"}
        for src in country_map:
            if src in df.columns and not df[src].isna().all():
                out["country_iso3"] = df[src].astype(str).str.upper().str[:3]
                break

        out["event_type"] = "battle_related_death"

        sev_map = {"best_estimate": "severity", "BestEstimate": "severity", "best": "severity",
                    "deaths": "severity", "Deaths": "severity", "low": "severity", "high": "severity"}
        for src in sev_map:
            if src in df.columns:
                out["severity"] = pd.to_numeric(df[src], errors="coerce")
                break

        out["lat"] = None
        out["lon"] = None
        out["source"] = "UCDP BRD"
        return out.dropna(subset=["event_id"])
