from hermes.core.cache import RawCache
from hermes.features import pipeline as features_pipeline


class Hermes:
    def __init__(
        self,
        cache_dir: str | None = None,
        use_cache: bool = True,
    ):
        self._cache = RawCache(cache_dir=cache_dir) if use_cache else None
        self.features = features_pipeline()

    def clear_cache(self, older_than: str | None = None):
        if self._cache:
            from datetime import timedelta
            td = None
            if older_than:
                unit = older_than[-1]
                val = int(older_than[:-1])
                if unit == "h":
                    td = timedelta(hours=val)
                elif unit == "d":
                    td = timedelta(days=val)
                elif unit == "w":
                    td = timedelta(weeks=val)
            self._cache.clear(older_than=td)

    def cache_stats(self) -> dict:
        if self._cache:
            return self._cache.stats()
        return {"total_files": 0, "by_source": {}, "hits": {}, "misses": {}, "hit_rate": {}}
