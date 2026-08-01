from collections.abc import Callable

from hermes.features.country_risk_features.economic import economic_features
from hermes.features.country_risk_features.environmental import enviromental_features
from hermes.features.country_risk_features.geopolitical import geopolitical_features
from hermes.features.country_risk_features.security import security_features
from hermes.features.country_risk_features.social import social_features


class features:
    def __init__(self):
        self.eco = economic_features()
        self.env = enviromental_features()
        self.geo = geopolitical_features()
        self.sec = security_features()
        self.soc = social_features()

    def list_features(self):
        list_featuress: list[Callable] = [
            self.eco.gdp_growth_yoy,
            self.eco.gdp_growth_qoq,
            self.eco.industrial_production_yoy,
            self.eco.inflation_cpi_yoy,
            self.eco.inflation_volatility_12m,
            self.eco.ppi_yoy,
            self.eco.inflation_yoy,
            self.eco.unemployment_rate,
            self.eco.youth_unemployment,
            self.eco.labor_force_participation,
            self.eco.current_account_gdp_ratio,
            self.eco.fx_reserves_months_import,
            self.eco.external_debt_gdp_ratio,
            self.eco.fiscal_deficit_gdp,
            self.eco.government_debt_gdp,
            self.eco.reer_misalignment,
            self.eco.banking_sector_health,
            self.eco.gdp_per_capita_ppp,
            self.geo.conflict_event_count_30d,
            self.geo.conflict_event_count_90d,
            self.geo.conflict_trend,
            self.geo.goldstein_scale_avg_30d,
            self.geo.goldstein_scale_trend,
            self.geo.battle_deaths_30d,
            self.geo.battle_deaths_90d,
            self.geo.protest_event_count_30d,
            self.geo.protest_violence_level,
            self.geo.diplomatic_event_count_30d,
            self.geo.diplomatic_intensity_avg,
            self.geo.sanctions_count_active,
            self.geo.sanctions_new_30d,
            self.geo.sanctions_sector_coverage,
            self.geo.governance_wgi_composite,
            self.geo.corruption_perception_index,
            self.geo.rule_of_law_score,
            self.geo.regulatory_quality,
            self.geo.democracy_index,
            self.geo.regime_type,
            self.geo.press_freedom_score,
            self.sec.military_spending_gdp,
            self.sec.military_spending_growth_yoy,
            self.sec.alliance_strength_score,
            self.sec.arms_imports_12m,
            self.sec.arms_exports_12m,
            self.sec.peacekeeping_troops,
            self.sec.nato_member,
            self.soc.social_stability_index,
            self.soc.human_rights_score,
            self.soc.fragile_state_index,
            self.soc.human_development_index,
            self.soc.gini_coefficient,
            self.soc.poverty_headcount_ratio,
            self.env.climate_vulnerability_score,
            self.env.climate_readiness_score,
            self.env.natural_disaster_risk,
            self.env.food_price_index_change_yoy,
            self.env.energy_dependence_ratio,
            self.env.water_stress_index,
        ]

        return list_featuress
