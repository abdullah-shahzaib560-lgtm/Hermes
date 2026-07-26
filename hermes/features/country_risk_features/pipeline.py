from datetime import datetime

from hermes.features.country_risk_features.economic import economic_features
from hermes.features.country_risk_features.environmental import enviromental_features
from hermes.features.country_risk_features.geopolitical import geopolitical_features
from hermes.features.country_risk_features.security import security_features
from hermes.features.country_risk_features.social import social_features

class pipeline:

    def __init__(self):
        self.eco = economic_features()
        self.env = enviromental_features()
        self.geo = geopolitical_features()
        self.sec = security_features()
        self.soc = social_features()

    def get_country_risk_features(self, country):
 

        return {
            "country": f"{country}",
            "economic": {
                "gdp_growth_yoy": self.eco.gdp_growth_yoy(),                                        # float, percent
                "gdp_growth_qoq": self.eco.gdp_growath_qoq(),                                       # float, percent
                "industrial_production_yoy": self.eco.industrial_production_yoy(),                  # float, percent
                "inflation_cpi_yoy": self.eco.inflation_cpi_yoy(),                                  # float, percent
                "inflation_volatility_12m": self.eco.inflation_volatility_12m(),                    # float, rolling std
                "ppi_yoy": self.eco.ppi_yoy(),                                                      # float, percent
                "unemployment_rate": self.eco.unemployment_rate(),                                  # float, percent
                "youth_unemployment": self.eco.youth_unemployment(),                                # float, percent
                "labor_force_participation": self.eco.labor_force_participation(),                  # float, percent
                "current_account_gdp_ratio": self.eco.current_account_gdp_ratio(),                  # float, percent of GDP
                "fx_reserves_months_import": self.eco.fx_reserves_months_import(),                  # float, months
                "external_debt_gdp_ratio": self.eco.external_debt_gdp_ratio(),                      # float, percent
                "fiscal_deficit_gdp": self.eco.fiscal_deficit_gdp(),                                # float, percent
                "government_debt_gdp": self.eco.government_debt_gdp(),                              # float, percent
                "credit_spread_bps": self.eco.credit_spread_bps(),                                  # int, basis points
                "yield_curve_10y_2y": self.eco.yield_curve_10y_2y(),                                # float, percentage points
                "banking_sector_health": self.eco.banking_sector_health(),                          # float, 0-1 score
                "gdp_per_capita_ppp": self.eco.gdp_per_capita_ppp(),                                # int, USD
            },
            "geopolitical": {
                "conflict_event_count_30d": self.geo.conflict_event_count_30d(),                    # int
                "conflict_event_count_90d": self.geo.conflict_event_count_90d(),                    # int
                "conflict_trend": self.geo.conflict_trend(),                                        # string: escalating/stable/de-escalating
                "goldstein_scale_avg_30d": self.geo.goldstein_scale_avg_30d(),                      # float, -10 to +10
                "goldstein_scale_trend": self.geo.goldstein_scale_trend(),                          # float, change vs prev period
                "battle_deaths_30d": self.geo.battle_deaths_30d(),                                  # int
                "battle_deaths_90d": self.geo.battle_deaths_90d(),                                  # int
                "protest_event_count_30d": self.geo.protest_event_count_30d(),                      # int
                "protest_violence_level": self.geo.protest_violence_level(),                        # float, 0-1
                "diplomatic_event_count_30d": self.geo.diplomatic_event_count_30d(),                # int
                "diplomatic_intensity_avg": self.geo.diplomatic_intensity_avg(),                    # float, 0-10 scale
                "sanctions_count_active": self.geo.sanctions_count_active(),                        # int
                "sanctions_new_30d": self.geo.sanctions_new_30d(),                                  # int
                "sanctions_sector_coverage": self.geo.sanctions_sector_coverage(),                  # float, 0-1
                "governance_wgi_composite": self.geo.governance_wgi_composite(),                    # float, -2.5 to +2.5
                "corruption_perception_index": self.geo.corruption_perception_index(),              # int, 0-100
                "rule_of_law_score": self.geo.rule_of_law_score(),                                  # float, -2.5 to +2.5
                "regulatory_quality": self.geo.regulatory_quality(),                                # float, -2.5 to +2.5
                "democracy_index": self.geo.democracy_index(),                                      # float, 0-1
                "regime_type": self.geo.regime_type(),                                              # string: democracy/hybrid/autocracy
                "press_freedom_score": self.geo.press_freedom_score(),                              # int, 0-100
            },
            "security": {
                "military_spending_gdp": self.sec.military_spending_gdp(),                          # float, percent
                "military_spending_growth_yoy": self.sec.military_spending_growth_yoy(),            # float, percent
                "alliance_strength_score": self.sec.alliance_strength_score(),                      # float, 0-1
                "arms_imports_12m": self.sec.arms_imports_12m(),                                    # int, millions USD
                "arms_exports_12m": self.sec.arms_exports_12m(),                                    # int, millions USD
                "peacekeeping_troops": self.sec.peacekeeping_troops(),                              # int
                "nato_member": self.sec.nato_member(),                                              # bool
            },
            "social": {
                "social_stability_index": self.soc.social_stability_index(),                        # float, 0-1
                "human_rights_score": self.soc.human_rights_score(),                                # float, 0-1
                "fragile_state_index": self.soc.fragile_state_index(),                              # float, 0-120
                "human_development_index": self.soc.human_development_index(),                      # float, 0-1
                "gini_coefficient": self.soc.gini_coefficient(),                                    # float, 0-100
                "poverty_headcount_ratio": self.soc.poverty_headcount_ratio(),                      # float, percent
            },
            "environmental": {
                "climate_vulnerability_score": self.env.climate_vulnerability_score(),              # float, 0-1
                "climate_readiness_score": self.env.climate_readiness_score(),                      # float, 0-1
                "natural_disaster_risk": self.env.natural_disaster_risk(),                          # float, 0-1
                "food_price_index_change_yoy": self.env.food_price_index_change_yoy(),              # float, percent
                "energy_dependence_ratio": self.env.energy_dependence_ratio(),                      # float, 0-1 (imports/consumption)
                "water_stress_index": self.env.water_stress_index(),                                # float, 0-1
            },
            "metadata": {
                "last_updated": f'{datetime.utcnow()}',               
                "features_version": "1.0.0",
            }
        }   