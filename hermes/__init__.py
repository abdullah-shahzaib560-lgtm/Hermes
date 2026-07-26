from hermes.sources.world_bank import World_Bank
from hermes.sources.imf import IMF
from hermes.sources.bis import BIS
from hermes.sources.comtrade import Comtrade
from hermes.sources.gdelt import GDELT
from hermes.sources.ucdp import UCDP
from hermes.sources.news_data import NewsData
from hermes.sources.v_dem import V_DEM
from hermes.sources.undp import UNDP
from hermes.sources.nd_gain import ND_GAIN
from hermes.sources.fao import FAO
from hermes.sources.fsi import FSI
from hermes.sources.sipri import SIPRI
from hermes.sources.cow import COW
from hermes.sources.un_peacekeeping import UN_Peacekeeping
from hermes.core.cache import RawCache
from hermes.features import pipeline as features_pipeline


class Hermes:
    def __init__(
        self,
        newsdata_api_key: str | None = None,
        comtrade_api_key: str | None = None,
        cache_dir: str | None = None,
        use_cache: bool = True,
    ):
        self._cache = RawCache(cache_dir=cache_dir) if use_cache else None

        self.world_bank = World_Bank(cache=self._cache)
        self.imf = IMF(cache=self._cache)
        self.bis = BIS(cache=self._cache)
        self.comtrade = Comtrade(api_key=comtrade_api_key, cache=self._cache)
        self.gdelt = GDELT(cache=self._cache)
        self.ucdp = UCDP(cache=self._cache)
        self.news_data = NewsData(api_key=newsdata_api_key, cache=self._cache)
        self.v_dem = V_DEM(cache=self._cache)
        self.undp = UNDP(cache=self._cache)
        self.nd_gain = ND_GAIN(cache=self._cache)
        self.fao = FAO(cache=self._cache)
        self.fsi = FSI(cache=self._cache)
        self.sipri = SIPRI(cache=self._cache)
        self.cow = COW(cache=self._cache)
        self.un_peacekeeping = UN_Peacekeeping(cache=self._cache)

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
