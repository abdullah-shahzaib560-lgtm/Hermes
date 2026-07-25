import numpy as np
import pandas as pd
import logging

logger = logging.getLogger(__name__)

class security_features:

    def military_spending_gdp(self, data) -> float:
        pass

    def military_spending_growth_yoy(self, data) -> float:
        pass

    def alliance_strength_score(self, data) -> float:
        pass

    def arms_imports_12m(self, data) -> int:
        pass

    def arms_exports_12m(self, data) -> int:
        pass
    
    def peacekeeping_troops(self, data) -> int:
        pass

    def nato_member(self, data) -> bool:
        pass