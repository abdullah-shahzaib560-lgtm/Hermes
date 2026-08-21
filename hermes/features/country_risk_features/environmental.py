import logging
from typing import Literal
import pandas as pd

from hermes.core.helper import adjust_year_range, check_empty
from hermes.core.feature_decorator import feature

from hermes.sources.world_bank import World_bank
from hermes.sources.public_data import PUBLIC_DATASET

logger = logging.getLogger(__name__)


class enviromental_features:
    def __init__(self):
        self.wb = World_bank()
        self._data = PUBLIC_DATASET()

    @feature(
        name="climate_vulnerability_score",
        group="enviromental_features",
        deps=["NDGAIN:cvs"],
        compute="climate vulnerability score computed from the NDGAIN dataset",
    )
    async def climate_vulnerability_score(self, country_code: str, mode: Literal["F", "ML"] = "F") -> float | pd.Series:
        data = await self._data.fetch_cvs(country=country_code)
        data = check_empty(data=data)
        if mode == "F":
            data = data.sort_values("year", ascending=False)
            return data["score"].iloc[0]
        if mode == "ML":
            data["year"] = data["year"].dt.year
            data = adjust_year_range(data, "year", 2000, 2025, fill_method="ffill")
            data = data.set_index("year")
            return data["score"]

    @feature(
        name="climate_readiness_score",
        group="enviromental_features",
        deps=["NDGAIN:crs"],
        compute="climate readiness score computed from the NDGAIN dataset",
    )
    async def climate_readiness_score(self, country_code: str, mode: Literal["F", "ML"] = "F") -> float | pd.Series:
        data = await self._data.fetch_crs(country=country_code)
        data = check_empty(data=data)
        if mode == "F":
            data = data.sort_values("year", ascending=False)
            return data["score"].iloc[0]
        if mode == "ML":
            data["year"] = data["year"].dt.year
            data = adjust_year_range(data, "year", 2000, 2025, fill_method="ffill")
            data = data.set_index("year")
            return data["score"]

    @feature(name="natural_disaster_risk", group="enviromental_features", deps=[], compute="")
    async def natural_disaster_risk(self, country_code: str, mode: Literal["F", "ML"] = "F") -> float: ...

    @feature(name="food_price_index_change_yoy", group="enviromental_features", deps=[], compute="")
    async def food_price_index_change_yoy(self, country_code: str, mode: Literal["F", "ML"] = "F") -> float: ...

    @feature(name="energy_dependence_ratio", group="enviromental_features", deps=[], compute="")
    async def energy_dependence_ratio(self, country_code: str, mode: Literal["F", "ML"] = "F") -> float:
        data = await self.wb.fetch(country_code=country_code, indicator_code="EG.IMP.CONS.ZS")
        data = check_empty(mode=mode, data=data, country=country_code)
        if mode == "F":
            data = data.sort_values("date", ascending=False)
            return data["value"].iloc[0]
        if mode == "ML":
            data["year"] = pd.to_datetime(data["date"]).dt.year
            data = adjust_year_range(data, "year", 2000, 2025, fill_method="ffill")
            data = data.set_index("date")
            return data["value"]

    @feature(name="water_stress_index", group="enviromental_features", deps=[], compute="")
    async def water_stress_index(self, country_code: str, mode: Literal["F", "ML"] = "F") -> float | pd.Series:
        data = await self.wb.fetch(country_code=country_code, indicator_code="ER.H2O.FWTL.ZS")
        data = check_empty(mode=mode, data=data, country=country_code)
        if mode == "F":
            data = data.sort_values("date", ascending=False)
            return data["value"].iloc[0]
        if mode == "ML":
            data["year"] = pd.to_datetime(data["date"]).dt.year
            data = adjust_year_range(data, "year", 2000, 2025, fill_method="ffill")
            data = data.set_index("date")
            return data["value"]


if __name__ == "__main__":
    import asyncio

    async def main():
        env = enviromental_features()
        data = await env.water_stress_index(country_code="PAK")
        print(data)

    asyncio.run(main())
