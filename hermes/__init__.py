from hermes.sources.bis import BIS
from hermes.sources.world_bank import World_Bank
from hermes.sources.imf import IMF

from hermes.sources.comtrade import Comtrade
from hermes.sources.gdelt import GDELT
from hermes.sources.ucdp import UCDP
from hermes.sources.news_data import NewsData


class Hermes:

    def __init__(
        self,
        newsdata_api_key: str | None = None,
    ):
        self.wb = World_Bank()
        self.world_bank = self.wb
        self.imf = IMF()
        self.bis = BIS()
        self.comtrade = Comtrade()
        self.gdelt = GDELT()
        self.ucdp = UCDP()
        self.news_data = NewsData(api_key=newsdata_api_key)