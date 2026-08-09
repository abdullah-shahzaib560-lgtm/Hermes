import logging
from typing import Literal

from hermes.sources.world_bank import World_bank

logger = logging.getLogger(__name__)

class enviromental_features:

    def __init__(self):
        self.wb = World_bank()

    async def climate_vulnerability_score(self, country_code: str, mode: str = Literal["F", "ML"]) -> float:
        pass

    async def climate_readiness_score(self, country_code: str, mode: str = Literal["F", "ML"]) -> float:
        pass

    async def natural_disaster_risk(self, country_code: str, mode: str = Literal["F", "ML"]) -> float:
        pass

    async def food_price_index_change_yoy(self, country_code: str, mode: str = Literal["F", "ML"]) -> float:
        pass

    async def energy_dependence_ratio(self, country_code: str, mode: str = Literal["F", "ML"]) -> float:
        pass

    async def water_stress_index(self, country_code: str) -> float:
        data = await self.wb.fetch(country_code=country_code, indicator_code='ER.H2O.FWTL.ZS')
        return data

if __name__ == '__main__':
    import asyncio

    async def main():
        env = enviromental_features()
        data = await env.water_stress_index(country_code='PAK')
        print(data)

    asyncio.run(main())
