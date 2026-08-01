import logging
from datetime import datetime

import pandas as pd

from hermes.features.country_risk_features.economic import economic_features
from hermes.features.country_risk_features.environmental import enviromental_features
from hermes.features.country_risk_features.geopolitical import geopolitical_features
from hermes.features.country_risk_features.security import security_features
from hermes.features.country_risk_features.social import social_features

logger = logging.getLogger(__name__)


class pipeline:
    def __init__(self, os_api: str):
        self.eco = economic_features()
        self.env = enviromental_features()
        self.geo = geopolitical_features(os_api=os_api)
        self.sec = security_features()
        self.soc = social_features()
        self.os_api = os_api

    def get_country_risk_features(self, country):

        return {
            "country": f"{country}",
            "economic": {
                "gdp_growth_yoy": self.eco.gdp_growth_yoy(country_code=country, mode="F"),
                "gdp_growth_qoq": self.eco.gdp_growth_qoq(country_code=country, mode="F"),
                "industrial_production_yoy": self.eco.industrial_production_yoy(
                    country_code=country, mode="F"
                ),  # float, percent
                "inflation_cpi_yoy": self.eco.inflation_cpi_yoy(country_code=country, mode="F"),  # float, percent
                "inflation_volatility_12m": self.eco.inflation_volatility_12m(
                    country_code=country, mode="F"
                ),  # float, rolling std
                "ppi_yoy": self.eco.ppi_yoy(country_code=country, mode="F"),  # float, percent
                "unemployment_rate": self.eco.unemployment_rate(country_code=country, mode="F"),  # float, percent
                "youth_unemployment": self.eco.youth_unemployment(country_code=country, mode="F"),  # float, percent
                "labor_force_participation": self.eco.labor_force_participation(
                    country_code=country, mode="F"
                ),  # float, percent
                "current_account_gdp_ratio": self.eco.current_account_gdp_ratio(
                    country_code=country, mode="F"
                ),  # float, percent of GDP
                "fx_reserves_months_import": self.eco.fx_reserves_months_import(
                    country_code=country, mode="F"
                ),  # float, months
                "external_debt_gdp_ratio": self.eco.external_debt_gdp_ratio(
                    country_code=country, mode="F"
                ),  # float, percent
                "fiscal_deficit_gdp": self.eco.fiscal_deficit_gdp(country_code=country, mode="F"),  # float, percent
                "government_debt_gdp": self.eco.government_debt_gdp(country_code=country, mode="F"),  # float, percent
                "reer_misalignment": self.eco.reer_misalignment(country_code=country, mode="F"),  # int, basis points
                "inflation_yoy": self.eco.inflation_yoy(country_code=country, mode="F"),  # float, percentage points
                "banking_sector_health": self.eco.banking_sector_health(
                    country_code=country, mode="F"
                ),  # float, 0-1 score
                "gdp_per_capita_ppp": self.eco.gdp_per_capita_ppp(country_code=country, mode="F"),  # int, USD
            },
            "geopolitical": {
                "conflict_event_count_30d": self.geo.conflict_event_count_30d(country_code=country, mode="F"),  # int
                "conflict_event_count_90d": self.geo.conflict_event_count_90d(country_code=country, mode="F"),  # int
                "conflict_trend": self.geo.conflict_trend(
                    country_code=country, mode="F"
                ),  # string: escalating/stable/de-escalating
                "goldstein_scale_avg_30d": self.geo.goldstein_scale_avg_30d(
                    country_code=country, mode="F"
                ),  # float, -10 to +10
                "goldstein_scale_trend": self.geo.goldstein_scale_trend(
                    country_code=country, mode="F"
                ),  # float, change vs prev period
                "battle_deaths_30d": self.geo.battle_deaths_30d(country_code=country, mode="F"),  # int
                "battle_deaths_90d": self.geo.battle_deaths_90d(country_code=country, mode="F"),  # int
                "protest_event_count_30d": self.geo.protest_event_count_30d(country_code=country, mode="F"),  # int
                "protest_violence_level": self.geo.protest_violence_level(country_code=country, mode="F"),  # float, 0-1
                "diplomatic_event_count_30d": self.geo.diplomatic_event_count_30d(
                    country_code=country, mode="F"
                ),  # int
                "diplomatic_intensity_avg": self.geo.diplomatic_intensity_avg(
                    country_code=country, mode="F"
                ),  # float, 0-10 scale
                "sanctions_count_active": self.geo.sanctions_count_active(country_code=country, mode="F"),  # int
                "sanctions_new_30d": self.geo.sanctions_new_30d(country_code=country, mode="F"),  # int
                "sanctions_sector_coverage": self.geo.sanctions_sector_coverage(
                    country_code=country, mode="F"
                ),  # float, 0-1
                "governance_wgi_composite": self.geo.governance_wgi_composite(
                    country_code=country, mode="F"
                ),  # float, -2.5 to +2.5
                "corruption_perception_index": self.geo.corruption_perception_index(
                    country_code=country, mode="F"
                ),  # int, 0-100
                "rule_of_law_score": self.geo.rule_of_law_score(country_code=country, mode="F"),  # float, -2.5 to +2.5
                "regulatory_quality": self.geo.regulatory_quality(
                    country_code=country, mode="F"
                ),  # float, -2.5 to +2.5
                "democracy_index": self.geo.democracy_index(country_code=country, mode="F"),  # float, 0-1
                "regime_type": self.geo.regime_type(
                    country_code=country, mode="F"
                ),  # string: democracy/hybrid/autocracy
                "press_freedom_score": self.geo.press_freedom_score(country_code=country, mode="F"),  # int, 0-100
            },
            "security": {
                "military_spending_gdp": self.sec.military_spending_gdp(
                    country_code=country, mode="F"
                ),  # float, percent
                "military_spending_growth_yoy": self.sec.military_spending_growth_yoy(
                    country_code=country, mode="F"
                ),  # float, percent
                "alliance_strength_score": self.sec.alliance_strength_score(
                    country_code=country, mode="F"
                ),  # float, 0-1
                "arms_imports_12m": self.sec.arms_imports_12m(country_code=country, mode="F"),  # int, millions USD
                "arms_exports_12m": self.sec.arms_exports_12m(country_code=country, mode="F"),  # int, millions USD
                "peacekeeping_troops": self.sec.peacekeeping_troops(country_code=country, mode="F"),  # int
                "nato_member": self.sec.nato_member(country_code=country),  # bool
            },
            "social": {
                "social_stability_index": self.soc.social_stability_index(country_code=country, mode="F"),  # float, 0-1
                "human_rights_score": self.soc.human_rights_score(country_code=country, mode="F"),  # float, 0-1
                "fragile_state_index": self.soc.fragile_state_index(country_code=country, mode="F"),  # float, 0-120
                "human_development_index": self.soc.human_development_index(
                    country_code=country, mode="F"
                ),  # float, 0-1
                "gini_coefficient": self.soc.gini_coefficient(country_code=country, mode="F"),  # float, 0-100
                "poverty_headcount_ratio": self.soc.poverty_headcount_ratio(
                    country_code=country, mode="F"
                ),  # float, percent
            },
            "environmental": {
                "climate_vulnerability_score": self.env.climate_vulnerability_score(
                    country_code=country, mode="F"
                ),  # float, 0-1
                "climate_readiness_score": self.env.climate_readiness_score(
                    country_code=country, mode="F"
                ),  # float, 0-1
                "natural_disaster_risk": self.env.natural_disaster_risk(country_code=country, mode="F"),  # float, 0-1
                "food_price_index_change_yoy": self.env.food_price_index_change_yoy(
                    country_code=country, mode="F"
                ),  # float, percent
                "energy_dependence_ratio": self.env.energy_dependence_ratio(
                    country_code=country, mode="F"
                ),  # float, 0-1 (imports/consumption)
                "water_stress_index": self.env.water_stress_index(country_code=country, mode="F"),  # float, 0-1
            },
            "metadata": {
                "last_updated": f"{datetime.utcnow()}",
                "features_version": "1.0.0",
            },
        }

    def build_training_panel(self, fns, countries):
        panels = []

        for country in countries:
            series_dict = {}

            for fn in fns:
                try:
                    series = fn(country, mode="ML")
                    # series is pd.Series with DatetimeIndex, monthly freq
                    if isinstance(series, pd.Series) and not series.empty:
                        series_dict[fn.__name__] = series
                except Exception as e:
                    logger.warning(f"{fn.__name__} failed for {country}: {e}")
                    continue

            if not series_dict:
                continue

            country_df = pd.DataFrame(series_dict)
            country_df["country_iso3"] = country
            country_df = country_df.reset_index().rename(columns={"index": "date"})
            country_df = country_df.set_index(["country_iso3", "date"])
            panels.append(country_df)

        if not panels:
            return pd.DataFrame()

        return pd.concat(panels).sort_index()
