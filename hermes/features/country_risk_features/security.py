import logging
from typing import Literal

logger = logging.getLogger(__name__)


class security_features:
    def military_spending_gdp(self, country_code: str, mode: str = Literal["F", "ML"]) -> float:
        pass

    def military_spending_growth_yoy(country_code: str, mode: str = Literal["F", "ML"]) -> float:
        pass

    def alliance_strength_score(self, country_code: str, mode: str = Literal["F", "ML"]) -> float:
        pass

    def arms_imports_12m(self, country_code: str, mode: str = Literal["F", "ML"]) -> int:
        pass

    def arms_exports_12m(self, country_code: str, mode: str = Literal["F", "ML"]) -> int:
        pass

    def peacekeeping_troops(self, country_code: str, mode: str = Literal["F", "ML"]) -> int:
        pass

    def nato_member(self, country_code: str) -> bool:
        nato_members = [
            "ALB",
            "BEL",
            "BGR",
            "CAN",
            "CZE",
            "DEU",
            "DNK",
            "ESP",
            "EST",
            "FIN",
            "FRA",
            "GBR",
            "GRC",
            "HRV",
            "HUN",
            "ISL",
            "ITA",
            "LTU",
            "LUX",
            "LVA",
            "MKD",
            "MNE",
            "NLD",
            "NOR",
            "POL",
            "PRT",
            "ROU",
            "SVK",
            "SVN",
            "SWE",
            "TUR",
            "USA",
        ]
        if country_code in nato_members:
            return True
        else:
            return False
