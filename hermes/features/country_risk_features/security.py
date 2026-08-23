import logging
from typing import Literal

import pandas as pd

from hermes.core.feature_decorator import feature
from hermes.core.helper import adjust_year_range
from hermes.sources.public_data import PUBLIC_DATASET

logger = logging.getLogger(__name__)


class security_features:
    def __init__(self):
        self._data = PUBLIC_DATASET()

    @feature(
        name="military_spending_gdp",
        group="security_features",
        deps=["sipri:milex"],
        compute="military_spending_gdp from the SIPRI dataset",
    )
    async def military_spending_gdp(self, country_code: str, mode: Literal["F", "ML"] = "F") -> float:
        data = await self._data.fetch_sipri(country=country_code)
        data["year"] = pd.to_datetime(data["year"]).dt.year

        if mode == "F":
            data = data.sort_values("year", ascending=False)
            return data["value"].iloc[0]
        if mode == "ML":
            data = adjust_year_range(data, "year", 2000, 2025, fill_method="ffill")
            data = data.set_index("year")
            return data["value"]

    @feature(
        name="military_spending_growth_yoy",
        group="security_features",
        deps=["sipri:milex"],
        compute="military_spending_growth_yoy from the SIPRI dataset",
    )
    async def military_spending_growth_yoy(
        self, country_code: str, mode: Literal["F", "ML"] = "F"
    ) -> float | pd.Series:

        data = await self._data.fetch_sipri(country=country_code)
        data = data.copy()

        data["year"] = pd.to_datetime(data["year"], format="%Y").dt.year
        data = data.set_index("year").sort_index(ascending=False)

        yoy = data["value"].pct_change(periods=1) * 100

        if mode == "F":
            latest = yoy.dropna()
            if latest.empty:
                return float("nan")
            return float(latest.iloc[1])
        if mode == "ML":
            yoy = yoy.reset_index()
            yoy = adjust_year_range(yoy, "year", 2000, 2025, fill_method="ffill")
            yoy = yoy.set_index("year")
            return yoy["value"]

        raise ValueError(f"Unsupported mode: {mode!r}")

    @feature(
        name="alliance_strength_score",
        group="security_features",
        deps=[],
        compute="alliance_strength_score",
    )
    async def alliance_strength_score(self, country_code: str, mode: Literal["F", "ML"] = "F") -> float:
        pass

    @feature(
        name="arms_imports_12m",
        group="security_features",
        deps=[],
        compute="arms_imports_12m",
    )
    async def arms_imports_12m(self, country_code: str, mode: Literal["F", "ML"] = "F") -> int:
        pass

    @feature(
        name="arms_exports_12m",
        group="security_features",
        deps=[],
        compute="arms_exports_12m",
    )
    async def arms_exports_12m(self, country_code: str, mode: Literal["F", "ML"] = "F") -> int:
        pass

    @feature(
        name="peacekeeping_troops",
        group="security_features",
        deps=[],
        compute="peacekeeping_troops",
    )
    async def peacekeeping_troops(self, country_code: str, mode: Literal["F", "ML"] = "F") -> int:
        pass

    @feature(
        name="nato_member",
        group="security_features",
        deps=["nato:membership"],
        compute="nato_member from the NATO dataset",
    )
    async def nato_member(self, country_code: str, mode: Literal["F", "ML"] = "F") -> bool:
        data = await self._data.fetch_nato(country=country_code)
        data["Year"] = pd.to_datetime(data["Year"]).dt.year

        if mode == "F":
            data = data.sort_values("Year", ascending=False)
            return bool(data["NATO Member"].iloc[0])
        elif mode == "ML":
            data = adjust_year_range(data, "Year", 2000, 2025, fill_method="ffill")
            data = data.set_index("Year")
            return data["NATO Member"]
