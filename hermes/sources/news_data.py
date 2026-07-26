import logging
from datetime import timedelta
import os
from typing import Optional

import pandas as pd
import urllib.parse
import urllib.request

from hermes.core.cache import RawCache

logger = logging.getLogger(__name__)

BASE_URL = "https://newsdata.io/api/1"


class NewsData:
    def __init__(self, api_key: Optional[str] = None, cache: RawCache | None = None):
        self.api_key = api_key or os.getenv("NEWSDATA_API_KEY")
        self._cache = cache

    def _fetch_json(self, endpoint: str, params: dict) -> dict:
        params["apikey"] = self.api_key
        qs = "&".join(f"{k}={urllib.parse.quote(str(v))}" for k, v in params.items() if v)
        url = f"{BASE_URL}/{endpoint}?{qs}"
        req = urllib.request.Request(url, headers={"User-Agent": "Hermes/0.1"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode())

    def _cached(self, params: dict, fetch_fn, force: bool = False):
        if self._cache is None:
            return fetch_fn()
        return self._cache.get_or_fetch("news_data", params, fetch_fn, force=force, ttl=timedelta(hours=1))

    def get_latest_news(
        self,
        q: Optional[str] = None,
        country: Optional[str] = None,
        category: Optional[str] = None,
        language: str = "en",
        page: Optional[str] = None,
        size: int = 50,
        normalize: bool = True,
        force: bool = False,
    ) -> pd.DataFrame:
        cache_params = {
            "q": "get_latest", "query": q or "", "country": country or "",
            "category": category or "", "lang": language, "page": page or "", "size": size,
        }

        def _fetch():
            params = {"language": language, "size": min(size, 50)}
            if q:
                params["q"] = q
            if country:
                params["country"] = country
            if category:
                params["category"] = category
            if page:
                params["page"] = page
            data = self._fetch_json("news", params)
            return pd.DataFrame(data.get("results", []))

        df = self._cached(cache_params, _fetch, force=force)
        if df.empty:
            return df
        return self._to_canonical(df) if normalize else df

    def get_archive_news(
        self,
        q: Optional[str] = None,
        country: Optional[str] = None,
        category: Optional[str] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        language: str = "en",
        page: Optional[str] = None,
        size: int = 50,
        normalize: bool = True,
        force: bool = False,
    ) -> pd.DataFrame:
        cache_params = {
            "q": "get_archive", "query": q or "", "country": country or "",
            "category": category or "", "from": from_date or "", "to": to_date or "",
            "lang": language, "page": page or "", "size": size,
        }

        def _fetch():
            params = {"language": language, "size": min(size, 50)}
            if q:
                params["q"] = q
            if country:
                params["country"] = country
            if category:
                params["category"] = category
            if from_date:
                params["from_date"] = from_date
            if to_date:
                params["to_date"] = to_date
            if page:
                params["page"] = page
            data = self._fetch_json("archive", params)
            return pd.DataFrame(data.get("results", []))

        df = self._cached(cache_params, _fetch, force=force)
        if df.empty:
            return df
        return self._to_canonical(df) if normalize else df

    def _to_canonical(self, df: pd.DataFrame) -> pd.DataFrame:
        if df.empty:
            return df
        col_map = {
            "article_id": "article_id", "link": "url", "pubDate": "date",
            "source_id": "source_name", "title": "title", "description": "content",
            "content": "content", "sentiment": "sentiment", "language": "lang",
        }
        rename = {k: v for k, v in col_map.items() if k in df.columns}
        df = df.rename(columns=rename)

        if "date" in df.columns:
            df["date"] = pd.to_datetime(df["date"], errors="coerce")

        for col, default in [("source_name", "newsdata"), ("sentiment", None), ("lang", None)]:
            if col not in df.columns:
                df[col] = default

        canonical = ["article_id", "date", "source_name", "title", "content", "sentiment", "url", "lang"]
        for col in canonical:
            if col not in df.columns:
                df[col] = None
        df["source"] = "NewsData.io"
        return df[canonical + ["source"]].reset_index(drop=True)
