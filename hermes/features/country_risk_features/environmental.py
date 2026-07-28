import numpy as np
import pandas as pd
import logging
from typing import Literal

logger = logging.getLogger(__name__)

class enviromental_features:

    def climate_vulnerability_score(self, country_code: str, mode: str = Literal['F', 'ML']) -> float:
        pass

    def climate_readiness_score(self, country_code: str, mode: str = Literal['F', 'ML']) -> float:
        pass

    def natural_disaster_risk(self, country_code: str, mode: str = Literal['F', 'ML']) -> float:
        pass

    def food_price_index_change_yoy(self, country_code: str, mode: str = Literal['F', 'ML']) -> float:
        pass

    def energy_dependence_ratio(self, country_code: str, mode: str = Literal['F', 'ML']) -> float:
        pass
    
    def water_stress_index(self, country_code: str, mode: str = Literal['F', 'ML']) -> float:
        pass