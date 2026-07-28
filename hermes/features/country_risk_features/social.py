import numpy as np
import pandas as pd
import logging

from typing import Literal

logger = logging.getLogger(__name__)

class social_features:

    def social_stability_index(self, country_code: str, mode: str = Literal['F', 'ML']) -> float:
        pass

    def human_rights_score(self, country_code: str, mode: str = Literal['F', 'ML']) -> float:
        pass

    def fragile_state_index(self, country_code: str, mode: str = Literal['F', 'ML']) -> float:
        pass

    def human_development_index(self, country_code: str, mode: str = Literal['F', 'ML']) -> float:
        pass

    def gini_coefficient(self, country_code: str, mode: str = Literal['F', 'ML']) -> float:
        pass
    
    def poverty_headcount_ratio(self, country_code: str, mode: str = Literal['F', 'ML']) -> float:
        pass