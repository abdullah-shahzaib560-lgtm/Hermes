import pandas as pd
import logging
import httpx
from typing import Optional

from hermes.core.cache import RawCache

logger = logging.getLogger(__name__)

API_BASE = "https://ucdpapi.uu.se/api/v1"


class UCDP:
    def __init__(self, cache: RawCache | None = None):
        self.base_url = API_BASE
        self._cache = cache

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
            "action": "get_ged_events",
            "country": country or "",
            "year_from": year_from or 0,
            "year_to": year_to or 0,
            "max_records": max_records,
        }

        def _fetch():
            params = {
                "pagesize": min(max_records, 10000),
                "page": 1,
            }
            if country:
                params["country"] = country
            if year_from:
                params["year_min"] = year_from
            if year_to:
                params["year_max"] = year_to

            all_records = []
            while True:
                url = f"{self.base_url}/ged/events"
                resp = httpx.get(url, params=params, timeout=60)
                resp.raise_for_status()
                data = resp.json()
                results = data.get("Result", data.get("results", []))
                if not results:
                    break
                all_records.extend(results)

                total_pages = data.get("TotalPages", data.get("totalPages", 1))
                if params["page"] >= total_pages:
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
            "action": "get_battle_related_deaths",
            "country": country or "",
            "year_from": year_from or 0,
            "year_to": year_to or 0,
        }

        def _fetch():
            params = {}
            if country:
                params["country"] = country
            if year_from:
                params["year_min"] = year_from
            if year_to:
                params["year_max"] = year_to

            url = f"{self.base_url}/brd/deaths"
            resp = httpx.get(url, params=params, timeout=60)
            resp.raise_for_status()
            data = resp.json()
            return pd.DataFrame(data.get("Result", data.get("results", [])))

        df = self._cached(cache_params, _fetch, force=force)
        if df.empty:
            return df
        return self._to_brd_canonical(df) if normalize else df

    def _to_ged_canonical(self, df: pd.DataFrame) -> pd.DataFrame:
        out = pd.DataFrame()
        id_col = df.get("id", df.get("event_id", df.get("Id", pd.NA)))
        if not id_col.isna().all():
            out["event_id"] = id_col.astype(str)
        else:
            out["event_id"] = None

        date_col = df.get(
            "date_start", df.get("date_end", df.get("DateStart", df.get("Date", pd.NA)))
        )
        if not date_col.isna().all():
            out["date"] = pd.to_datetime(date_col, errors="coerce")
        else:
            out["date"] = pd.NaT

        country_col = df.get(
            "country", df.get("Country", df.get("country_iso3", pd.NA))
        )
        if not country_col.isna().all():
            if country_col.dtype == object:
                out["country_iso3"] = country_col.str.upper().str[:3]
            else:
                out["country_iso3"] = country_col.astype(str).str.upper().str[:3]
        else:
            out["country_iso3"] = None

        type_col = df.get(
            "type_of_violence", df.get("event_type", df.get("TypeOfViolence", pd.NA))
        )
        if not type_col.isna().all():
            out["event_type"] = type_col.astype(str)
        else:
            out["event_type"] = "armed_conflict"

        severity_col = df.get(
            "best", df.get("deaths_civilians", df.get("Best", df.get("Deaths", pd.NA)))
        )
        if not severity_col.isna().all():
            out["severity"] = pd.to_numeric(severity_col, errors="coerce")
        else:
            out["severity"] = None

        lat_col = df.get("latitude", df.get("Latitude", df.get("lat", pd.NA)))
        if not lat_col.isna().all():
            out["lat"] = pd.to_numeric(lat_col, errors="coerce")
        else:
            out["lat"] = None

        lon_col = df.get("longitude", df.get("Longitude", df.get("lon", pd.NA)))
        if not lon_col.isna().all():
            out["lon"] = pd.to_numeric(lon_col, errors="coerce")
        else:
            out["lon"] = None

        out["source"] = "UCDP GED"
        return out.dropna(subset=["event_id"])

    def _to_brd_canonical(self, df: pd.DataFrame) -> pd.DataFrame:
        out = pd.DataFrame()
        id_col = df.get("id", df.get("Id", pd.NA))
        if not id_col.isna().all():
            out["event_id"] = id_col.astype(str)
        else:
            out["event_id"] = None

        year_col = df.get("year", df.get("Year", pd.NA))
        if not year_col.isna().all():
            out["date"] = pd.to_datetime(
                year_col.astype(str) + "-01-01", errors="coerce"
            )
        else:
            out["date"] = pd.NaT

        country_col = df.get(
            "country", df.get("Country", df.get("location", pd.NA))
        )
        if not country_col.isna().all():
            if country_col.dtype == object:
                out["country_iso3"] = country_col.str.upper().str[:3]
            else:
                out["country_iso3"] = country_col.astype(str).str.upper().str[:3]

        out["event_type"] = "battle_related_death"

        deaths_col = df.get(
            "best_estimate", df.get("BestEstimate", df.get("deaths", df.get("Deaths", pd.NA)))
        )
        if not deaths_col.isna().all():
            out["severity"] = pd.to_numeric(deaths_col, errors="coerce")

        out["lat"] = None
        out["lon"] = None
        out["source"] = "UCDP BRD"
        return out.dropna(subset=["event_id"])
