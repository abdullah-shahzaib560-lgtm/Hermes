import numpy as np
import pandas as pd
import logging
from hermes.core.feature_decorator import feature
import pycountry

from typing import Literal

logger = logging.getLogger(__name__)


from hermes.sources.world_bank import World_bank


def check_iso3(code):
    country = pycountry.countries.get(alpha_3=code.upper())
    if not country:
        logger.error('The Country Code should be in iso3')
        raise 

class economic_features:

    def __init__(self):
        self.wb = World_bank()

    @feature(
        name='gdp_growth_yoy',
        group='economic_features',
        deps=['world_bank:NY.GDP.MKTP.KD.ZG'],
        compute='GDP growth YoY, merged from WB and IMF'
    )
    def gdp_growth_yoy(self, country_code: str, mode: Literal['ML', 'Frontend']):

        check_iso3(code=country_code)

        data = self.wb.fetch(country_code=country_code, indicator_code='NY.GDP.MKTP.KD.ZG')

        if mode == 'Frontend':
            return data["value"].iloc[0]
        return data["value"]



    @feature(
        name='gdp_growth_qoq',
        group='economic_features',
        deps=['world_bank:NY.GDP.MKTP.KD'],
        compute='GDP growth QoQ, interpolated from the the annual frequency data from the World_Bank'
    )
    def gdp_growth_qoq(self, country_code: str, mode: Literal['ML', 'Frontend']):
        check_iso3(code=country_code)
        data = self.wb.fetch(country_code=country_code, indicator_code='NY.GDP.MKTP.KD')
        data["date"] = pd.to_datetime(data["date"].astype(str) + "-12-31")
        meta = data[["indicator_id", "indicator_name", "country", "source"]].iloc[0]

        data = data.set_index("date")
        df = data[["value"]].resample("QE").interpolate(method="linear")
        df["gdp_growth_qoq"] = df["value"].pct_change() * 100

        for col in ["indicator_id", "indicator_name", "country", "source"]:
            df[col] = meta[col]

        df = df.drop(columns=["value"]).reset_index().sort_values("date", ascending=False)

        if mode == 'Frontend':
            return df["gdp_growth_qoq"].iloc[0]
        return df

    @feature(
            name='industrial_production_yoy',
            group='economic_features',
            deps=['world_bank:NV.IND.MANF.KD.ZG'],
            compute='industrial_production_yoy from the World Bank data'
    )    
    def industrial_production_yoy(self, country_code: str) -> float:
        check_iso3(code=country_code)
        data = self.wb.fetch(country_code=country_code, indicator_code='NV.IND.MANF.KD.ZG')
        return data

    @feature(
            name='inflation_cpi_yoy',
            group='economic_features',
            deps=['world_bank:NV.IND.MANF.KD.ZG'],
            compute='industrial_production_yoy from the World Bank data'
    )    
    def inflation_cpi_yoy(self, country_code: str) -> float:
        check_iso3(code=country_code)
        data = self.wb.fetch(country_code=country_code, indicator_code='SL.UEM.TOTL.ZS')
        return data

    @feature(
            name='inflation_volatility_12m',
            group='economic_features',
            deps=['world_bank:NV.IND.MANF.KD.ZG'],
            compute='industrial_production_yoy from the World Bank data'
    )    
    def inflation_volatility_12m(self, country_code: str) -> float:
        check_iso3(code=country_code)
        data = self.wb.fetch(country_code=country_code, indicator_code='SL.UEM.TOTL.ZS')
        return data

    @feature(
            name='ppi_yoy',
            group='economic_features',
            deps=['world_bank:NV.IND.MANF.KD.ZG'],
            compute='industrial_production_yoy from the World Bank data'
    )    
    def ppi_yoy(self, country_code: str) -> float:
        check_iso3(code=country_code)
        ...
        return data

    @feature(
            name='unemployment_rate',
            group='economic_features',
            deps=['world_bank:NV.IND.MANF.KD.ZG'],
            compute='industrial_production_yoy from the World Bank data'
    )    
    def unemployment_rate(self, country_code: str) -> float:
        check_iso3(code=country_code)
        data = self.wb.fetch(country_code=country_code, indicator_code='SL.UEM.TOTL.ZS')
        return data

    @feature(
            name='youth_unemployment',
            group='economic_features',
            deps=['world_bank:NV.IND.MANF.KD.ZG'],
            compute='industrial_production_yoy from the World Bank data'
    )    
    def youth_unemployment(self, country_code: str) -> float:
        check_iso3(code=country_code)
        data = self.wb.fetch(country_code=country_code, indicator_code='SL.UEM.1524.ZS')
        return data

    @feature(
            name='labor_force_participation',
            group='economic_features',
            deps=['world_bank:NV.IND.MANF.KD.ZG'],
            compute='industrial_production_yoy from the World Bank data'
    )    
    def labor_force_participation(self, country_code: str) -> float:
        check_iso3(code=country_code)
        data = self.wb.fetch(country_code=country_code, indicator_code='SL.TLF.CACT.ZS')
        return data

    @feature(
            name='current_account_gdp_ratio',
            group='economic_features',
            deps=['world_bank:NV.IND.MANF.KD.ZG'],
            compute='industrial_production_yoy from the World Bank data'
    )    
    def current_account_gdp_ratio(self, country_code: str) -> float:
        check_iso3(code=country_code)
        data = self.wb.fetch(country_code=country_code, indicator_code='BN.CAB.XOKA.GD.ZS')
        return data

    @feature(
            name='fx_reserves_months_import',
            group='economic_features',
            deps=['world_bank:NV.IND.MANF.KD.ZG'],
            compute='industrial_production_yoy from the World Bank data'
    )    
    def fx_reserves_months_import(self ,country_code: str) -> float:
        check_iso3(code=country_code)
        data = self.wb.fetch(country_code=country_code, indicator_code='FI.RES.TOTL.MO')
        return data

    @feature(
            name='external_debt_gdp_ratio',
            group='economic_features',
            deps=['world_bank:NV.IND.MANF.KD.ZG'],
            compute='industrial_production_yoy from the World Bank data'
    )    
    def external_debt_gdp_ratio(self, country_code: str) -> float:
        check_iso3(code=country_code)
        data = self.wb.fetch(country_code=country_code, indicator_code='DT.DOD.DECT.GN.ZS')
        return data

    @feature(
            name='fiscal_deficit_gdp',
            group='economic_features',
            deps=['world_bank:NV.IND.MANF.KD.ZG'],
            compute='industrial_production_yoy from the World Bank data'
    )    
    def fiscal_deficit_gdp(self, country_code: str) -> float:
        check_iso3(code=country_code)
        ...
        return data

    @feature(
            name='government_debt_gdp',
            group='economic_features',
            deps=['world_bank:NV.IND.MANF.KD.ZG'],
            compute='industrial_production_yoy from the World Bank data'
    )    
    def government_debt_gdp(self, country_code: str) -> float:
        check_iso3(code=country_code)
        ...
        return data

    @feature(
            name='credit_spread_bps',
            group='economic_features',
            deps=['world_bank:NV.IND.MANF.KD.ZG'],
            compute='industrial_production_yoy from the World Bank data'
    )    
    def credit_spread_bps(self, country_code: str) -> float:
        check_iso3(code=country_code)
        ...
        return data

    @feature(
            name='yield_curve_10y_2y',
            group='economic_features',
            deps=['world_bank:NV.IND.MANF.KD.ZG'],
            compute='industrial_production_yoy from the World Bank data'
    )    
    def yield_curve_10y_2y(self, country_code: str) -> float:
        check_iso3(code=country_code)
        ...
        return data

    @feature(
            name='banking_sector_health',
            group='economic_features',
            deps=['world_bank:NV.IND.MANF.KD.ZG'],
            compute='industrial_production_yoy from the World Bank data'
    )    
    def banking_sector_health(self, country_code: str) -> float:
        check_iso3(code=country_code)
        data = self.wb.fetch(country_code=country_code, indicator_code='FB.AST.NPLN.ZS')
        return data

    @feature(
            name='gdp_per_capita_ppp',
            group='economic_features',
            deps=['world_bank:NV.IND.MANF.KD.ZG'],
            compute='industrial_production_yoy from the World Bank data'
    )    
    def gdp_per_capita_ppp(self, country_code: str) -> float:
        check_iso3(code=country_code)
        data = self.wb.fetch(country_code=country_code, indicator_code='NY.GDP.PCAP.PP.CD')
        return data


if __name__ == '__main__':
    eco = economic_features()
    data = eco.industrial_production_yoy(country_code='USA')
    print(data)