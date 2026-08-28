from hermes.constants import CANONICAL_FREQS as CANONICAL_FREQS
from hermes.constants import SYMBOLS as SYMBOLS
from hermes.constants import TICKERS as TICKERS

from hermes.core.cache import RawCache
from hermes.entities.countries import countries
from hermes.core.features import features

from hermes.features import pipeline as features_pipeline
from hermes.features.financial.crpto import CryptoHistory
from hermes.features.financial.filling import CompanyFiling
from hermes.features.financial.fundamental import FAfeatures
from hermes.features.financial.technical import TAfeatures

from hermes.sources.binance import Binance
from hermes.sources.finnhub import FINNHUB
from hermes.sources.fred import FRED
from hermes.sources.gdelt import GDELT
from hermes.sources.imf import IMF
from hermes.sources.opensanctions import OpenSanction
from hermes.sources.public_data import PUBLIC_DATASET
from hermes.sources.sec_edgar import SECEDGAR
from hermes.sources.world_bank import World_bank
from hermes.sources.yf import Yfinance


class Hermes:
    def __init__(
        self,
        opensanction_api: str,
        new_data_api: str,
        fred_api: str,
        sec_username: str,
        sec_email: str,
        finnhub_api: str,
        cache_dir: str | None = None,
        use_cache: bool = True,
    ):
        if not opensanction_api and not new_data_api:
            raise KeyError("Add Opensanction API, NewsDataAPI for full usage")

        self._cache = RawCache(cache_dir=cache_dir) if use_cache else None
        self.list_countries = countries
        self.lf = features(os_api=opensanction_api)
        self.list_features = self.lf.list_features()

        self.gdelt = GDELT()
        self.imf = IMF(cache=self._cache)
        self.opensanction = OpenSanction(api_key=opensanction_api, cache=self._cache)
        self.world_bank = World_bank(cache=self._cache)
        self.fred = FRED(api=fred_api, cache=self._cache)
        self.binance = Binance(cache=self._cache)
        self.sec_edger = SECEDGAR(username=sec_username, email=sec_email, cache=self._cache)
        self.finnhub = FINNHUB(api=finnhub_api, cache=self._cache)
        self.yfin = Yfinance(cache=self._cache)
        self.datasets = PUBLIC_DATASET()

        self.country_features = features_pipeline(os_api=opensanction_api)
        self.ta_feature = TAfeatures()
        self.fa_features = FAfeatures(
            finnhub_api=finnhub_api,
            fred_api=fred_api,
            sec_username=sec_username,
            sec_email=sec_email,
        )
        self.crypto_history = CryptoHistory()
        self.filling_history = CompanyFiling(
            finnhub_api=finnhub_api,
            sec_email=sec_email,
            sec_username=sec_username,
            fred_api=fred_api,
        )

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
