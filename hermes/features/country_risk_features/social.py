import logging
from typing import Literal
import pandas as pd

from hermes.sources.world_bank import World_bank
from hermes.sources.hdi import VDEMHDI

from hermes.core.helper import check_empty

logger = logging.getLogger(__name__)


class social_features:

    def __init__(self):
        self.wb = World_bank()
        self.hdi = VDEMHDI()

    def social_stability_index(self, country_code: str, mode: str = Literal["F", "ML"]) -> float:
        ...

    def human_rights_score(self, country_code: str, mode: str = Literal["F", "ML"]) -> float:
        pass

    def fragile_state_index(self, country_code: str, mode: str = Literal["F", "ML"]) -> float:
        pass

    def human_development_index(self, country_code: str, mode: str = Literal["F", "ML"]) -> float:
        data = self.hdi.fetch(country=country_code)
        data = check_empty(data=data)
        
        data = data.set_index('Year')
        data.sort_index(inplace=True)
        data.resample("MS")

        if mode == 'F':
            return data['HDI'].iloc[0]
        if mode == 'ML':
            return data['HDI']

    def gini_coefficient(self, country_code: str, mode: str = Literal["F", "ML"]) -> float:
        data = self.wb.fetch(country_code=country_code, indicator_code='SI.POV.GINI')
        data = check_empty(data=data)

        data = data.set_index('date')
        data.index = pd.to_datetime('date')
        data.sort_index(inplace=True)
        data.resample("MS").interpolate()
        if mode == 'F':
            return data['value'].iloc[0]
        if mode == 'ML':
            return data['value']

    def poverty_headcount_ratio(self, country_code: str, mode: str = Literal["F", "ML"]) -> float:
        data = self.wb.fetch(country_code=country_code, indicator_code='SI.POV.DDAY')
        data = check_empty(data=data)

        data = data.set_index('date')
        data.index = pd.to_datetime('date')
        data.sort_index(inplace=True)
        data.resample("MS").interpolate()
        if mode == 'F':
            return data['value'].iloc[0]
        if mode == 'ML':
            return data['value']
