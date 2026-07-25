import pandas as pd
import logging
import httpx
from typing import Optional

from hermes.core.cache import RawCache

logger = logging.getLogger(__name__)

BASE_URL = "https://api.gdeltproject.org/api/v2"


class GDELT:
    def __init__(self, cache: RawCache | None = None):
        self.base_url = BASE_URL
        self._cache = cache

    def _cached(self, params: dict, fetch_fn, force: bool = False):
        if self._cache is None:
            return fetch_fn()
        return self._cache.get_or_fetch("gdelt", params, fetch_fn, force=force)

    def query_events(
        self,
        query: str = "",
        countries: Optional[list[str]] = None,
        themes: Optional[list[str]] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        max_records: int = 250,
        normalize: bool = True,
        force: bool = False,
    ) -> pd.DataFrame:
        terms = []
        if query:
            terms.append(query)
        if countries:
            for c in countries:
                terms.append(f"sourcecountry:{c}")
        if themes:
            for t in themes:
                terms.append(f"theme:{t}")

        full_query = " ".join(terms) if terms else " " 
        params = {
            "query": full_query,
            "mode": "artlist",
            "format": "json",
            "maxrecords": min(max_records, 250),
        }
        if start_date:
            params["startdatetime"] = start_date
        if end_date:
            params["enddatetime"] = end_date

        url = f"{self.base_url}/doc/doc"
        resp = httpx.get(url, params=params, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        articles = data.get("articles", data.get("results", []))
        cache_params = {
            "action": "query_events",
            "query": query or "",
            "countries": ",".join(countries) if countries else "",
            "themes": ",".join(themes) if themes else "",
            "start_date": start_date or "",
            "end_date": end_date or "",
            "max_records": max_records,
        }

        def _fetch():
            terms = []
            if query:
                terms.append(query)
            if countries:
                for c in countries:
                    terms.append(f"sourcecountry:{c}")
            if themes:
                for t in themes:
                    terms.append(f"theme:{t}")

            full_query = " ".join(terms) if terms else " "
            params = {
                "query": full_query,
                "mode": "artlist",
                "format": "json",
                "maxrecords": min(max_records, 250),
            }
            if start_date:
                params["startdatetime"] = start_date
            if end_date:
                params["enddatetime"] = end_date

            url = f"{self.base_url}/doc/doc"
            resp = httpx.get(url, params=params, timeout=30)
            resp.raise_for_status()
            data = resp.json()
            return pd.DataFrame(data.get("articles", data.get("results", [])))

        df = self._cached(cache_params, _fetch, force=force)
        if df.empty:
            return df
        return self._to_canonical(df) if normalize else df

    def query_gkg(
        self,
        query: str = "",
        countries: Optional[list[str]] = None,
        themes: Optional[list[str]] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        max_records: int = 250,
        normalize: bool = True,
        force: bool = False,
    ) -> pd.DataFrame:
        terms = []
        if query:
            terms.append(query)
        if countries:
            for c in countries:
                terms.append(f"sourcecountry:{c}")
        if themes:
            for t in themes:
                terms.append(f"theme:{t}")

        full_query = " ".join(terms) if terms else " "
        params = {
            "query": full_query,
            "mode": "gkg",
            "format": "json",
            "maxrecords": min(max_records, 250),
        }
        if start_date:
            params["startdatetime"] = start_date
        if end_date:
            params["enddatetime"] = end_date

        url = f"{self.base_url}/doc/doc"
        resp = httpx.get(url, params=params, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        gkg_entries = data.get("gkg", data.get("results", []))
        cache_params = {
            "action": "query_gkg",
            "query": query or "",
            "countries": ",".join(countries) if countries else "",
            "themes": ",".join(themes) if themes else "",
            "start_date": start_date or "",
            "end_date": end_date or "",
            "max_records": max_records,
        }

        def _fetch():
            terms = []
            if query:
                terms.append(query)
            if countries:
                for c in countries:
                    terms.append(f"sourcecountry:{c}")
            if themes:
                for t in themes:
                    terms.append(f"theme:{t}")

            full_query = " ".join(terms) if terms else " "
            params = {
                "query": full_query,
                "mode": "gkg",
                "format": "json",
                "maxrecords": min(max_records, 250),
            }
            if start_date:
                params["startdatetime"] = start_date
            if end_date:
                params["enddatetime"] = end_date

            url = f"{self.base_url}/doc/doc"
            resp = httpx.get(url, params=params, timeout=30)
            resp.raise_for_status()
            data = resp.json()
            return pd.DataFrame(data.get("gkg", data.get("results", [])))

        df = self._cached(cache_params, _fetch, force=force)
        if df.empty:
            return df
        return self._to_gkg_canonical(df) if normalize else df

    def get_event_timeline(
        self,
        query: str = "",
        countries: Optional[list[str]] = None,
        themes: Optional[list[str]] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        normalize: bool = True,
        force: bool = False,
    ) -> pd.DataFrame:
        terms = []
        if query:
            terms.append(query)
        if countries:
            for c in countries:
                terms.append(f"sourcecountry:{c}")
        if themes:
            for t in themes:
                terms.append(f"theme:{t}")

        full_query = " ".join(terms) if terms else " "
        params = {
            "query": full_query,
            "mode": "timelinevolraw",
            "format": "json",
            "timelinesmooth": "0",
        }
        if start_date:
            params["startdatetime"] = start_date
        if end_date:
            params["enddatetime"] = end_date

        url = f"{self.base_url}/doc/doc"
        resp = httpx.get(url, params=params, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        timeline = data.get("timeline", data.get("results", []))
        cache_params = {
            "action": "get_event_timeline",
            "query": query or "",
            "countries": ",".join(countries) if countries else "",
            "themes": ",".join(themes) if themes else "",
            "start_date": start_date or "",
            "end_date": end_date or "",
        }

        def _fetch():
            terms = []
            if query:
                terms.append(query)
            if countries:
                for c in countries:
                    terms.append(f"sourcecountry:{c}")
            if themes:
                for t in themes:
                    terms.append(f"theme:{t}")

            full_query = " ".join(terms) if terms else " "
            params = {
                "query": full_query,
                "mode": "timelinevolraw",
                "format": "json",
                "timelinesmooth": "0",
            }
            if start_date:
                params["startdatetime"] = start_date
            if end_date:
                params["enddatetime"] = end_date

            url = f"{self.base_url}/doc/doc"
            resp = httpx.get(url, params=params, timeout=30)
            resp.raise_for_status()
            data = resp.json()
            return pd.DataFrame(data.get("timeline", data.get("results", [])))

        df = self._cached(cache_params, _fetch, force=force)
        if df.empty:
            return df
        return self._to_timeline_canonical(df) if normalize else df

    def _to_canonical(self, df: pd.DataFrame) -> pd.DataFrame:
        out = pd.DataFrame()
        col_map = {
            "url": "url",
            "title": "title",
            "seendate": "date",
            "domain": "source_name",
            "themes": "themes",
            "tone": "sentiment",
            "language": "lang",
        }
        available = {k: v for k, v in col_map.items() if k in df.columns}
        out = df.rename(columns=available)

        if "date" in out.columns:
            out["date"] = pd.to_datetime(out["date"].astype(str).str[:10], errors="coerce")

        out["article_id"] = None
        out["content"] = out.get("title", None)
        if "url" in df.columns:
            out["url"] = df["url"]
        else:
            out["url"] = None
        if "source_name" not in out.columns:
            out["source_name"] = "GDELT"
        if "sentiment" in out.columns:
            out["sentiment"] = pd.to_numeric(out["sentiment"], errors="coerce")
        else:
            out["sentiment"] = None
        if "lang" not in out.columns:
            out["lang"] = None

        canonical_cols = [
            "article_id", "date", "source_name", "title",
            "content", "sentiment", "url", "lang",
        ]
        keep = [c for c in canonical_cols if c in out.columns]
        out = out[keep]
        out["source"] = "GDELT"
        return out

    def _to_gkg_canonical(self, df: pd.DataFrame) -> pd.DataFrame:
        out = pd.DataFrame()
        col_map = {
            "date": "date",
            "domain": "source_name",
            "name": "title",
            "value": "value",
            "themes": "themes",
            "tone": "sentiment",
            "numarticles": "article_count",
        }
        available = {k: v for k, v in col_map.items() if k in df.columns}
        out = df.rename(columns=available)

        if "date" in out.columns:
            out["date"] = pd.to_datetime(
                out["date"].astype(str).str[:10], errors="coerce"
            )
        out["source"] = "GDELT GKG"
        return out

    def _to_timeline_canonical(self, df: pd.DataFrame) -> pd.DataFrame:
        out = pd.DataFrame()
        date_col = df.get("date", df.get("time", pd.NA))
        if not date_col.isna().all():
            out["date"] = pd.to_datetime(date_col, errors="coerce")
        elif "key" in df.columns:
            out["date"] = pd.to_datetime(df["key"].astype(str).str[:10], errors="coerce")

        val_col = df.get("value", df.get("count", df.get("Value", pd.NA)))
        if not val_col.isna().all():
            out["value"] = pd.to_numeric(val_col, errors="coerce")

        out["source"] = "GDELT"
        return out.dropna(subset=["date"])
