import pandas as pd
import httpx
import logging
import os
from datetime import datetime, timedelta
from typing import Optional

logger = logging.getLogger(__name__)

BASE_URL = "https://newsdata.io/api/1"


class NewsData:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("NEWSDATA_API_KEY")

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

        data = self._request("news", params)
        articles = data.get("results", [])
        df = pd.DataFrame(articles)
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

        data = self._request("archive", params)
        articles = data.get("results", [])
        df = pd.DataFrame(articles)
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
