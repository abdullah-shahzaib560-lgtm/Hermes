import numpy as np
import pandas as pd
import logging
from typing import Literal
logger = logging.getLogger(__name__)

class geopolitical_features:

    def conflict_event_count_30d(self, data) -> int:
        pass

    def conflict_event_count_90d(self, data) -> int:
        pass

    def conflict_trend(self, data) -> Literal['escalating','stable','de-escalating']:
        pass

    def goldstein_scale_avg_30d(self, data) -> float:
        pass

    def goldstein_scale_trend(self, data) -> float:
        pass
    
    def battle_deaths_30d(self, data) -> int:
        pass

    def battle_deaths_90d(self, data) -> int:
        pass

    def protest_event_count_30d(self, data) -> int:
        pass

    def protest_violence_level(self, data) -> float:
        pass

    def diplomatic_event_count_30d(self, data) -> int:
        pass

    def diplomatic_intensity_avg(self ,data) -> float:
        pass

    def sanctions_count_active(self, data) -> int:
        pass

    def sanctions_new_30d(self, data) -> int:
        pass

    def sanctions_sector_coverage(self, data) -> float:
        pass

    def governance_wgi_composite(self, data) -> float:
        pass

    def corruption_perception_index(self, data) -> int:
        pass

    def rule_of_law_score(self, data) -> float:
        pass

    def regulatory_quality(self, data) -> float:
        pass

    def democracy_index(self, data) -> float:
        pass

    def regime_type(self, data) -> Literal['democracy','hybrid','autocracy']:
        pass

    def press_freedom_score(self, data) -> int:
        pass