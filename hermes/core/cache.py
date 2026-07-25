import hashlib
import json
import logging
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd

logger = logging.getLogger(__name__)

DEFAULT_CACHE_DIR = Path.home() / ".hermes_cache" / "raw"

TTL_BY_SOURCE = {
    "world_bank": timedelta(hours=24),
    "imf": timedelta(hours=24),
    "bis": timedelta(hours=24),
    "comtrade": timedelta(hours=24),
    "gdelt": timedelta(hours=6),
    "ucdp": timedelta(hours=24),
    "news_data": timedelta(hours=1),
}


class CacheMiss(Exception):
    pass


class RawCache:
    def __init__(self, cache_dir: str | Path | None = None):
        self.cache_dir = Path(cache_dir) if cache_dir else DEFAULT_CACHE_DIR
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def _source_dir(self, source: str) -> Path:
        p = self.cache_dir / source
        p.mkdir(parents=True, exist_ok=True)
        return p

    def _key_path(self, source: str, params: dict) -> Path:
        raw = f"{source}:{json.dumps(params, sort_keys=True, default=str)}"
        h = hashlib.sha256(raw.encode()).hexdigest()[:16]
        return self._source_dir(source) / f"{h}.parquet"

    def _meta_path(self, source: str, params: dict) -> Path:
        raw = f"{source}:{json.dumps(params, sort_keys=True, default=str)}"
        h = hashlib.sha256(raw.encode()).hexdigest()[:16]
        return self._source_dir(source) / f"{h}.meta.json"

    def get(self, source: str, params: dict) -> pd.DataFrame:
        path = self._key_path(source, params)
        if not path.exists():
            raise CacheMiss(f"No cache for {source}:{params}")

        mtime = datetime.fromtimestamp(path.stat().st_mtime)
        ttl = TTL_BY_SOURCE.get(source, timedelta(hours=24))
        age = datetime.now() - mtime

        if age > ttl:
            logger.debug(f"Cache expired for {source}:{params} (age={age})")
            raise CacheMiss(f"Cache expired for {source}:{params}")

        df = pd.read_parquet(path)
        logger.debug(f"Cache HIT for {source}:{params}")
        return df

    def put(self, source: str, params: dict, df: pd.DataFrame):
        path = self._key_path(source, params)
        df.to_parquet(path, index=False)
        meta = {
            "source": source,
            "params": params,
            "cached_at": datetime.now().isoformat(),
            "rows": len(df),
            "columns": list(df.columns),
        }
        meta_path = self._meta_path(source, params)
        meta_path.write_text(json.dumps(meta, indent=2, default=str))
        logger.debug(f"Cached {len(df)} rows for {source}:{params}")

    def get_or_fetch(
        self,
        source: str,
        params: dict,
        fetch_fn,
        force: bool = False,
    ) -> pd.DataFrame:
        if not force:
            try:
                return self.get(source, params)
            except CacheMiss:
                pass

        df = fetch_fn()
        if df is not None and not df.empty:
            self.put(source, params, df)
        return df

    def clear(self, older_than: timedelta | None = None):
        now = datetime.now()
        removed = 0
        for p in self.cache_dir.rglob("*.parquet"):
            age = now - datetime.fromtimestamp(p.stat().st_mtime)
            if older_than is None or age > older_than:
                p.unlink()
                meta = p.with_suffix(".meta.json")
                if meta.exists():
                    meta.unlink()
                removed += 1
        logger.info(f"Cleared {removed} cache files")

    def stats(self) -> dict:
        total = 0
        by_source = {}
        for p in self.cache_dir.rglob("*.parquet"):
            total += 1
            source = p.parent.name
            by_source[source] = by_source.get(source, 0) + 1
        return {"total_files": total, "by_source": by_source}
