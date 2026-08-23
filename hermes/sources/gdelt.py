import asyncio
import io
import json
import logging
import zipfile
from datetime import datetime, timedelta
from functools import partial
from typing import Any
from urllib.parse import urlencode

import aiohttp
import pandas as pd

from hermes.core.cache import RawCache
from hermes.sources.lib.fips import FIPS_TO_ISO3, ISO3_TO_FIPS
from hermes.sources.lib.gdlet_help import (
    CANONICAL_COLUMNS,
    EVENT_THEMES,
    GDELT_DOC_API,
    GDELT_EVENT_COLUMNS,
    GDELT_MASTER,
    GKG_EVENT_TYPES,
)

logger = logging.getLogger(__name__)


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

    async def _fetch_via_doc_api(
        self,
        countries: list[str] | None = None,
        themes: list[str] | None = None,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
        timeout: float = 30.0,
        retries: int = 4,
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

        resp = None
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=timeout)) as client:
            for attempt in range(retries):
                try:
                    resp = await client.get(url)
                    resp.raise_for_status()
                    text = await resp.text()
                    if text.lstrip().startswith("<") or "html" in resp.content_type.lower():
                        logger.warning("GDELT Doc API returned HTML (rate limited), retry %d", attempt + 1)
                        if attempt == retries - 1:
                            return pd.DataFrame()
                        await asyncio.sleep(5 * (attempt + 1))
                        continue
                    data = json.loads(text)
                    break
                except (TimeoutError, aiohttp.ClientResponseError) as e:
                    if isinstance(e, aiohttp.ClientResponseError) and e.status != 429:
                        raise
                    if attempt == retries - 1:
                        raise
                    logger.warning("GDELT Doc API %s, retry %d", type(e).__name__, attempt + 1)
                    await asyncio.sleep(5 * (attempt + 1))

        if resp is None:
            logger.warning("GDELT Doc API: all retries failed for: %s", query[:200])
            return pd.DataFrame()

        articles = data.get("articles", data.get("result", []))
        if not articles:
            logger.info("GDELT Doc API returned 0 articles for: %s", query[:200])
            return pd.DataFrame()

        df = pd.DataFrame(articles)
        logger.info("GDELT Doc API returned %d articles", len(df))
        return df

    async def _load_master_list(self, timeout: float = 60.0) -> pd.DataFrame:
        if self._master_df is not None:
            return self._master_df
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=timeout)) as client:
            resp = await client.get(GDELT_MASTER)
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

    async def _urls_in_range(self, start: datetime, end: datetime) -> list[str]:
        master = await self._load_master_list()
        mask = (master["timestamp"] >= start) & (master["timestamp"] <= end)
        return master.loc[mask, "url"].tolist()

    async def _download_one(self, url: str, timeout: float = 30.0, retries: int = 3) -> pd.DataFrame:
        resp = None
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=timeout)) as client:
            for attempt in range(retries):
                try:
                    resp = await client.get(url)
                    resp.raise_for_status()
                    break
                except (TimeoutError, aiohttp.ClientResponseError) as e:
                    if isinstance(e, aiohttp.ClientResponseError):
                        if e.status == 404:
                            logger.warning("404 for %s", url)
                            return pd.DataFrame(columns=GDELT_EVENT_COLUMNS)
                        raise
                    if attempt == retries - 1:
                        raise
        with zipfile.ZipFile(io.BytesIO(resp.content)) as zf:
            inner = zf.namelist()[0]
            with zf.open(inner) as f:
                return pd.read_csv(f, sep="\t", header=None, names=GDELT_EVENT_COLUMNS, dtype=str)

    async def _fetch_via_exports(
        self,
        country_code: str,
        start_date: datetime,
        end_date: datetime,
        max_workers: int = 8,
        max_files: int = 96,
    ) -> pd.DataFrame:
        urls = await self._urls_in_range(start_date, end_date)
        if not urls:
            logger.warning("No GDELT files in range %s - %s", start_date, end_date)
            return pd.DataFrame(columns=GDELT_EVENT_COLUMNS)
        if len(urls) > max_files:
            logger.warning("Range covers %d files - capping to last %d", len(urls), max_files)
            urls = urls[-max_files:]

        semaphore = asyncio.Semaphore(max_workers)

        async def _download(url: str) -> pd.DataFrame:
            async with semaphore:
                return await self._download_one(url)

        results = await asyncio.gather(
            *(_download(u) for u in urls),
            return_exceptions=True,
        )

        frames: list[pd.DataFrame] = []
        for url, result in zip(urls, results):
            if isinstance(result, Exception):
                logger.exception("Download failed for %s: %s", url, result)
                continue
            if not result.empty:
                frames.append(result)

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

    async def query_events(
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

        df = await self._cache.get_or_fetch(
            source="gdelt",
            params=cache_params,
            fetch_fn=partial(
                self._fetch_via_doc_api,
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
