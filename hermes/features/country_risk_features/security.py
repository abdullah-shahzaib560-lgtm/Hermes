import logging
from typing import Literal

from hermes.sources.public_data import PUBLIC_DATASET

logger = logging.getLogger(__name__)


class security_features:
    def __init__(self):
        self._data = PUBLIC_DATASET()

    async def military_spending_gdp(self, country_code: str, mode: str = Literal["F", "ML"]) -> float: ...

    async def military_spending_growth_yoy(country_code: str, mode: str = Literal["F", "ML"]) -> float:
        pass

    async def alliance_strength_score(self, country_code: str, mode: str = Literal["F", "ML"]) -> float:
        pass

    async def arms_imports_12m(self, country_code: str, mode: str = Literal["F", "ML"]) -> int:
        pass

    async def arms_exports_12m(self, country_code: str, mode: str = Literal["F", "ML"]) -> int:
        pass

    async def peacekeeping_troops(self, country_code: str, mode: str = Literal["F", "ML"]) -> int:
        pass

    async def nato_member(self, country_code: str) -> bool:
        data = await self._data.fetch_nato(country=country_code)
        return bool((data["NATO Member"] == 1).any())
