import pandas as pd
import logging
import urllib.request
import urllib.parse
import json
from typing import Optional

from hermes.core.cache import RawCache

logger = logging.getLogger(__name__)

BASE_URL = "https://api.gdeltproject.org/api/v2/doc/doc"


class GDELT:
    def __init__(self, cache: RawCache | None = None):
        self._cache = cache

    def _fetch_json(self, url: str) -> dict:
        req = urllib.request.Request(url, headers={"User-Agent": "Hermes/0.1"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode())

    def _cached(self, params: dict, fetch_fn, force: bool = False):
        if self._cache is None:
            return fetch_fn()
        return self._cache.get_or_fetch("gdelt", params, fetch_fn, force=force)

    def _build_query(self, query: str = "", countries: Optional[list[str]] = None,
                     themes: Optional[list[str]] = None) -> str:
        terms = []
        if query:
            terms.append(query)
        if countries:
            for c in countries:
                terms.append(f"sourcecountry:{c}")
        if themes:
            for t in themes:
                terms.append(f"theme:{t}")
        return " ".join(terms) if terms else " "

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
        cache_params = {
            "q": "query_events", "query": query or "",
            "countries": ",".join(countries) if countries else "",
            "themes": ",".join(themes) if themes else "",
            "start": start_date or "", "end": end_date or "",
            "max": max_records,
        }

        def _fetch():
            full_query = self._build_query(query, countries, themes)
            params = {
                "query": full_query, "mode": "artlist", "format": "json",
                "maxrecords": min(max_records, 250),
            }
            if start_date:
                params["startdatetime"] = start_date
            if end_date:
                params["enddatetime"] = end_date
            qs = "&".join(f"{k}={urllib.parse.quote(str(v))}" for k, v in params.items())
            url = f"{BASE_URL}?{qs}"
            data = self._fetch_json(url)
            articles = data.get("articles", data.get("results", []))
            return pd.DataFrame(articles)

        df = self._cached(cache_params, _fetch, force=force)
        if df.empty:
            return df
        return self._to_media_canonical(df) if normalize else df

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
        cache_params = {
            "q": "query_gkg", "query": query or "",
            "countries": ",".join(countries) if countries else "",
            "themes": ",".join(themes) if themes else "",
            "start": start_date or "", "end": end_date or "",
            "max": max_records,
        }

        def _fetch():
            full_query = self._build_query(query, countries, themes)
            params = {
                "query": full_query, "mode": "gkg", "format": "json",
                "maxrecords": min(max_records, 250),
            }
            if start_date:
                params["startdatetime"] = start_date
            if end_date:
                params["enddatetime"] = end_date
            qs = "&".join(f"{k}={urllib.parse.quote(str(v))}" for k, v in params.items())
            url = f"{BASE_URL}?{qs}"
            data = self._fetch_json(url)
            return pd.DataFrame(data.get("gkg", data.get("results", [])))

        df = self._cached(cache_params, _fetch, force=force)
        if df.empty:
            return df
        return df

    def _to_media_canonical(self, df: pd.DataFrame) -> pd.DataFrame:
        out = pd.DataFrame()
        col_map = {
            "url": "url", "title": "title", "seendate": "date",
            "domain": "source_name", "tone": "sentiment", "language": "lang",
        }
        for src, dst in col_map.items():
            if src in df.columns:
                out[dst] = df[src]

        if "date" in out.columns:
            dates = out["date"].astype(str)
            dates = dates.str.extract(r"(\d{4})(\d{2})(\d{2})", expand=False)
            if not dates.isna().all().all():
                out["date"] = pd.to_datetime(
                    dates[0] + "-" + dates[1] + "-" + dates[2], errors="coerce"
                )
            else:
                out["date"] = pd.to_datetime(out["date"], errors="coerce")

        out["article_id"] = df.get("url", df.get("id", None))
        out["content"] = out.get("title", None)
        if "sentiment" in out.columns:
            out["sentiment"] = pd.to_numeric(out["sentiment"], errors="coerce")
        if "source_name" not in out.columns:
            out["source_name"] = "GDELT"
        if "lang" not in out.columns:
            out["lang"] = None

        cols = ["article_id", "date", "source_name", "title", "content", "sentiment", "url", "lang"]
        keep = [c for c in cols if c in out.columns]
        out = out[keep]
        out["source"] = "GDELT"
        return out
