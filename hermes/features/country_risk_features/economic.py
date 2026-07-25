import numpy as np
import pandas as pd
import logging
from ...core.feature_decorator import feature
logger = logging.getLogger(__name__)

class economic_features:
    @feature(
        name='gdp_growth_yoy',
        group='economic_features',
        deps=['world_bank:'],
        compute='GDP growth YoY, merged from WB and IMF'
    )
    def gdp_growth_yoy(self, data) -> float:
        pass

    def gdp_growath_qoq(self, data) -> float:
        pass

    def industrial_production_yoy(self, data) -> float:
        pass

    def inflation_cpi_yoy(self, data) -> float:
        pass

    def inflation_volatility_12m(self, data) -> float:
        pass
    
    def ppi_yoy(self, data) -> float:
        pass

    def unemployment_rate(self, data) -> float:
        pass

    def youth_unemployment(self, data) -> float:
        pass

    def labor_force_participation(self, data) -> float:
        pass

    def current_account_gdp_ratio(self, data) -> float:
        pass

    def fx_reserves_months_import(self ,data) -> float:
        pass

    def external_debt_gdp_ratio(self, data) -> float:
        pass

    def fiscal_deficit_gdp(self, data) -> float:
        pass

    def government_debt_gdp(self, data) -> float:
        pass

    def credit_spread_bps(self, data) -> int:
        pass

    def yield_curve_10y_2y(self, data) -> float :
        pass

    def banking_sector_health(self, data) -> float:
        pass

    def gdp_per_capita_ppp(self, data) -> int:
        pass