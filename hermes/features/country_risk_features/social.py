import logging
from typing import Literal

import pandas as pd

from hermes.core.helper import check_empty
from hermes.sources.public_data import PUBLIC_DATASET
from hermes.sources.world_bank import World_bank

logger = logging.getLogger(__name__)


class social_features:
    def __init__(self):
        self.wb = World_bank()
        self._data = PUBLIC_DATASET()

    async def social_stability_index(self, country_code: str, mode: str = Literal["F", "ML"]) -> float: ...

    async def human_rights_score(self, country_code: str, mode: str = Literal["F", "ML"]) -> float:
        data = await self._data.fetch_hrs(country=country_code)
        data = check_empty(data=data, mode=mode)
        data = data.set_index('date')
        data.sort_index(inplace=True)
        data = data.resample("MS")
        if mode == 'F':
            return data['human_right_score'].iloc[0]
        if mode == 'ML':
            return data['human_right_score']

    async def fragile_state_index(self, country_code: str, mode: str = Literal["F", "ML"]) -> float:
        data = await self._data.fetch_fsi(country=country_code)
        data = check_empty(data=data, mode=mode)
        data = data.set_index('date')
        data.sort_index(inplace=True)
        data = data.resample('MS')
        if mode == 'F':
            return data['Total'].iloc[0]
        if mode == 'ML':
            return data['Total']

    async def human_development_index(self, country_code: str, mode: str = Literal["F", "ML"]) -> float:
        data = await self._data.fetch_hdi(country=country_code)
        data = check_empty(data=data, mode=mode)
        data = data.set_index("Year")
        data.sort_index(inplace=True)
        data.resample("MS")
        if mode == "F":
            return data["HDI"].iloc[0]
        if mode == "ML":
            return data["HDI"]

    async def gini_coefficient(self, country_code: str, mode: str = Literal["F", "ML"]) -> float:
        data = await self.wb.fetch(country_code=country_code, indicator_code="SI.POV.GINI")
        data = check_empty(data=data, mode=mode)

        data = data.set_index("date")
        data.index = pd.to_datetime("date")
        data.sort_index(inplace=True)
        data.resample("MS").interpolate()
        if mode == "F":
            return data["value"].iloc[0]
        if mode == "ML":
            return data["value"]

    async def poverty_headcount_ratio(self, country_code: str, mode: str = Literal["F", "ML"]) -> float:
        data = await self.wb.fetch(country_code=country_code, indicator_code="SI.POV.DDAY")
        data = check_empty(data=data, mode=mode)

        data = data.set_index("date")
        data.index = pd.to_datetime("date")
        data.sort_index(inplace=True)
        data.resample("MS").interpolate()
        if mode == "F":
            return data["value"].iloc[0]
        if mode == "ML":
            return data["value"]
