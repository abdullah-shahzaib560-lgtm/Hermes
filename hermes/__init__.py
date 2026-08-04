from hermes.core.cache import RawCache
from hermes.core.countries import countries
from hermes.core.features import features
from hermes.features import pipeline as features_pipeline
from hermes.sources.gdelt import GDELT
from hermes.sources.imf import IMF
from hermes.sources.opensanctions import OpenSanction
from hermes.sources.world_bank import World_bank


class Hermes:
    def __init__(
        self,
        opensanction_api: str,
        new_data_api: str,
        cache_dir: str | None = None,
        use_cache: bool = True,
    ):
        if not opensanction_api and not new_data_api:
            raise KeyError("Add Opensanction API, NewsDataAPI for full usage")

        self._cache = RawCache(cache_dir=cache_dir) if use_cache else None
        self.features = features_pipeline(os_api=opensanction_api)
        self.gdelt = GDELT()
        self.imf = IMF()
        self.opensanction = OpenSanction(api_key=opensanction_api)
        self.world_bank = World_bank()
        self.list_countries = countries
        self.lf = features(os_api=opensanction_api)
        self.list_features = self.lf.list_features()

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
