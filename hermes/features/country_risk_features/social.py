import logging
from typing import Literal

import pandas as pd

from hermes.core.helper import adjust_year_range, check_empty
from hermes.core.feature_decorator import feature
from hermes.sources.public_data import PUBLIC_DATASET
from hermes.sources.world_bank import World_bank

logger = logging.getLogger(__name__)


class social_features:
    def __init__(self):
        self.wb = World_bank()
        self._data = PUBLIC_DATASET()

    @feature(
        name="social_stability_index",
        group="social_features",
        deps=[],
        compute="social_stability_index",
    )
    async def social_stability_index(self, country_code: str, mode: Literal["F", "ML"] = "F") -> float: ...

    @feature(
        name="human_rights_score",
        group="social_features",
        deps=["hrs:human_rights"],
        compute="human_rights_score from the Human Rights Score dataset",
    )
    async def human_rights_score(self, country_code: str, mode: Literal["F", "ML"] = "F") -> float:
        data = await self._data.fetch_hrs(country=country_code)
        data = check_empty(data=data, mode=mode)
        if mode == "F":
            data = data.sort_values("date", ascending=False)
            return data["human_right_score"].iloc[0]
        if mode == "ML":
            data["year"] = data["date"].dt.year
            data = adjust_year_range(data, "year", 2000, 2025, fill_method="ffill")
            data = data.set_index("date")
            return data["human_right_score"]

    @feature(
        name="fragile_state_index",
        group="social_features",
        deps=["fsi:fragile_states"],
        compute="fragile_state_index from the Fragile States Index dataset",
    )
    async def fragile_state_index(self, country_code: str, mode: Literal["F", "ML"] = "F") -> float:
        data = await self._data.fetch_fsi(country=country_code)
        data = check_empty(data=data, mode=mode)
        if mode == "F":
            data = data.sort_values("date", ascending=False)
            return data["Total"].iloc[0]
        if mode == "ML":
            data["year"] = data["date"].dt.year
            data = adjust_year_range(data, "year", 2000, 2025, fill_method="ffill")
            data = data.set_index("date")
            return data["Total"]

    @feature(
        name="human_development_index",
        group="social_features",
        deps=["hdi:human_development"],
        compute="human_development_index from the HDI dataset",
    )
    async def human_development_index(self, country_code: str, mode: Literal["F", "ML"] = "F") -> float:
        data = await self._data.fetch_hdi(country=country_code)
        data = check_empty(data=data, mode=mode)
        if mode == "F":
            data = data.sort_values("Year", ascending=False)
            return data["HDI"].iloc[0]
        if mode == "ML":
            data["year"] = data["Year"].dt.year
            data = adjust_year_range(data, "year", 2000, 2025, fill_method="ffill")
            data = data.set_index("Year")
            return data["HDI"]

    @feature(
        name="gini_coefficient",
        group="social_features",
        deps=["world_bank:SI.POV.GINI"],
        compute="gini_coefficient from the World Bank data",
    )
    async def gini_coefficient(self, country_code: str, mode: Literal["F", "ML"] = "F") -> float:
        data = await self.wb.fetch(country_code=country_code, indicator_code="SI.POV.GINI")
        data = check_empty(data=data, mode=mode)

        if mode == "F":
            data = data.sort_values("date", ascending=False)
            return data["value"].iloc[0]
        if mode == "ML":
            data["year"] = pd.to_datetime(data["date"]).dt.year
            data = adjust_year_range(data, "year", 2000, 2025, fill_method="ffill")
            data = data.set_index("date")
            return data["value"]

    @feature(
        name="poverty_headcount_ratio",
        group="social_features",
        deps=["world_bank:SI.POV.DDAY"],
        compute="poverty_headcount_ratio from the World Bank data",
    )
    async def poverty_headcount_ratio(self, country_code: str, mode: Literal["F", "ML"] = "F") -> float:
        data = await self.wb.fetch(country_code=country_code, indicator_code="SI.POV.DDAY")
        data = check_empty(data=data, mode=mode)

        if mode == "F":
            data = data.sort_values("date", ascending=False)
            return data["value"].iloc[0]
        if mode == "ML":
            data["year"] = pd.to_datetime(data["date"]).dt.year
            data = adjust_year_range(data, "year", 2000, 2025, fill_method="ffill")
            data = data.set_index("date")
            return data["value"]
