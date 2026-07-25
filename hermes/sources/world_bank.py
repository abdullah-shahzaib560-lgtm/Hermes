import pandas as pd
import logging
import httpx
from typing import Optional

logger = logging.getLogger(__name__)

BASE_URL = "https://api.worldbank.org/v2"


class World_Bank:
    def __init__(self):
        self.base_url = BASE_URL

    def get_data(
        self,
        indicator: str,
        country: str = "all",
        date: Optional[str] = None,
        per_page: int = 5000,
        normalize: bool = True,
    ) -> pd.DataFrame:
        records = []
        page = 1
        while True:
            params = {
                "format": "json",
                "per_page": min(per_page, 1000),
                "page": page,
            }
            if date:
                params["date"] = date

            url = f"{self.base_url}/country/{country}/indicator/{indicator}"
            resp = httpx.get(url, params=params, timeout=30)
            resp.raise_for_status()
            data = resp.json()

            if not data or len(data) < 2:
                break

            records.extend(data[1])
            total_pages = data[0].get("pages", 1)
            if page >= total_pages:
                break
            page += 1

        df = pd.DataFrame(records)
        if df.empty:
            return df
        return self._to_canonical(df) if normalize else df

    def search_indicators(self, query: str, per_page: int = 100) -> pd.DataFrame:
        url = f"{self.base_url}/indicator"
        params = {"format": "json", "search": query, "per_page": per_page}
        resp = httpx.get(url, params=params, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        if not data or len(data) < 2:
            return pd.DataFrame()
        rows = []
        for item in data[1]:
            rows.append({
                "indicator_id": item.get("id"),
                "name": item.get("name"),
                "source_note": item.get("sourceNote"),
            })
        return pd.DataFrame(rows)

    def _to_canonical(self, df: pd.DataFrame) -> pd.DataFrame:
        out = pd.DataFrame()
        out["date"] = pd.to_datetime(
            df.get("date", pd.NA), format="%Y", errors="coerce"
        )
        out["country_iso3"] = df.get("countryiso3code", pd.NA)
        out["indicator_id"] = df.get("indicator", {}).apply(
            lambda x: x.get("id") if isinstance(x, dict) else pd.NA
        )
        out["value"] = pd.to_numeric(df.get("value", pd.NA), errors="coerce")
        out["source"] = "World Bank"
        return out.dropna(subset=["date", "country_iso3", "indicator_id"])
