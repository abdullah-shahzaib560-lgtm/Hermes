import pandas as pd
import httpx
import logging
import os
from typing import Optional

from hermes.core.cache import RawCache

logger = logging.getLogger(__name__)

BASE_URL = "https://newsdata.io/api/1"


class NewsData:
    def __init__(self, api_key: Optional[str] = None, cache: RawCache | None = None):
        self.api_key = api_key or os.getenv("NEWSDATA_API_KEY")
        self._cache = cache

    def _cached(self, params: dict, fetch_fn, force: bool = False):
        if self._cache is None:
            return fetch_fn()
        return self._cache.get_or_fetch("news_data", params, fetch_fn, force=force)

    def _request(self, endpoint: str, params: dict) -> dict:
        params["apikey"] = self.api_key
        url = f"{BASE_URL}/{endpoint}"
        resp = httpx.get(url, params=params, timeout=30)
        resp.raise_for_status()
        return resp.json()

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
        params = {
            "language": language,
            "size": min(size, 50),
        }
        if q:
            params["q"] = q
        if country:
            params["country"] = country
        if category:
            params["category"] = category
        if page:
            params["page"] = page

        cache_params = {
            "action": "get_latest_news",
            "q": q or "",
            "country": country or "",
            "category": category or "",
            "language": language,
            "page": page or "",
            "size": size,
        }

        def _fetch():
            data = self._request("news", params)
            return pd.DataFrame(data.get("results", []))

        df = self._cached(cache_params, _fetch, force=force)
        return self._to_canonical(df) if normalize and not df.empty else df

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
        params = {
            "language": language,
            "size": min(size, 50),
        }
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

        cache_params = {
            "action": "get_archive_news",
            "q": q or "",
            "country": country or "",
            "category": category or "",
            "from_date": from_date or "",
            "to_date": to_date or "",
            "language": language,
            "page": page or "",
            "size": size,
        }

        def _fetch():
            data = self._request("archive", params)
            return pd.DataFrame(data.get("results", []))

        df = self._cached(cache_params, _fetch, force=force)
        return self._to_canonical(df) if normalize and not df.empty else df

    def _to_canonical(self, df: pd.DataFrame) -> pd.DataFrame:
        col_map = {
            "article_id": "article_id",
            "link": "url",
            "pubDate": "date",
            "source_id": "source_name",
            "title": "title",
            "description": "content",
            "content": "content",
            "sentiment": "sentiment",
            "language": "lang",
            "country": "country_iso3",
        }
        available = {k: v for k, v in col_map.items() if k in df.columns}
        df = df.rename(columns=available)

        if "date" in df.columns:
            df["date"] = pd.to_datetime(df["date"], errors="coerce")

        if "source_name" not in df.columns:
            df["source_name"] = "newsdata"
        if "sentiment" not in df.columns:
            df["sentiment"] = None
        if "lang" not in df.columns and "language" in df.columns:
            df["lang"] = df["language"]

        canonical_cols = [
            "article_id", "date", "source_name", "title",
            "content", "sentiment", "url", "lang",
        ]
        keep = [c for c in canonical_cols if c in df.columns]
        df = df[keep]
        df["source"] = "NewsData.io"
        return df
