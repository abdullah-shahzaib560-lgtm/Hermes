import numpy as np
import pandas as pd
import logging
from hermes.core.feature_decorator import feature
import pycountry

from typing import Literal

logger = logging.getLogger(__name__)


from hermes.sources.world_bank import World_bank
from hermes.sources.imf import IMF

def check_iso3(code):
    country = pycountry.countries.get(alpha_3=code.upper())
    if not country:
        logger.error('The Country Code should be in iso3')
        raise 

class economic_features:

    def __init__(self):
        self.wb = World_bank()
        self.imf = IMF()

    @feature(
        name='gdp_growth_yoy',
        group='economic_features',
        deps=['world_bank:NY.GDP.MKTP.KD.ZG'],
        compute='GDP growth YoY, merged from WB and IMF'
    )
    def gdp_growth_yoy(self, country_code: str, mode:str = Literal['ML', 'Frontend']):

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
    def gdp_growth_qoq(self, country_code: str, mode: str = Literal['ML', 'Frontend']):
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
        return df['gdp_growth_qoq']

    @feature(
            name='industrial_production_yoy',
            group='economic_features',
            deps=['world_bank:NV.IND.MANF.KD.ZG'],
            compute='industrial_production_yoy from the World Bank data'
    )    
    def industrial_production_yoy(self, country_code: str, mode: str = Literal['ML', 'Frontend']) -> float:
        check_iso3(code=country_code)
        data = self.wb.fetch(country_code=country_code, indicator_code='NV.IND.MANF.KD.ZG')
        if mode == 'ML':
            return data['value']
        if mode == 'Frontend':
            return data['value'].iloc[0]


    @feature(
            name='inflation_cpi_yoy',
            group='economic_features',
            deps=['world_bank:SL.UEM.TOTL.ZS'],
            compute='inflation_cpi_yoy from the World Bank data'
    )    
    def inflation_cpi_yoy(self, country_code: str,  mode: str = Literal['ML', 'Frontend']) -> float:
        check_iso3(code=country_code)
        data = self.wb.fetch(country_code=country_code, indicator_code='SL.UEM.TOTL.ZS')
        if mode == 'ML':
            return data['value']
        if mode == 'Frontend':
            return data['value'].iloc[0]

    @feature(
            name='inflation_volatility_12m',
            group='economic_features',
            deps=['world_bank:SL.UEM.TOTL.ZS'],
            compute='inflation_volatility_12m from the World Bank data'
    )    
    def inflation_volatility_12m(self, country_code: str,  mode: str = Literal['ML', 'Frontend']) -> float:
        check_iso3(code=country_code)
        data = self.wb.fetch(country_code=country_code, indicator_code='SL.UEM.TOTL.ZS')
        if mode == 'ML':
            return data['value']
        if mode == 'Frontend':
            return data['value'].iloc[0]

        
    @feature(
            name='inflation_yoy',
            group='economic_features',
            deps=['world_bank:NV.IND.MANF.KD.ZG'],
            compute='inflation_yoy from the IMF data'
    )    
    def inflation_yoy(self, country_code: str, mode: str = Literal['ML', 'Frontend']) -> float:
        check_iso3(code=country_code)
        data = self.imf.fetch(country=country_code, agency='IMF.STA', dataflow_id='CPI', key='CPI._T.IX.M')
        if mode == 'ML':
            return data['value']
        if mode == 'Frontend':
            return data['value'].iloc[0]

    @feature(
            name='unemployment_rate',
            group='economic_features',
            deps=['world_bank:SL.UEM.TOTL.ZS'],
            compute='unemployment_rate from the World Bank data'
    )    
    def unemployment_rate(self, country_code: str, mode: str = Literal['ML', 'F']) -> float:
        check_iso3(code=country_code)
        data = self.wb.fetch(country_code=country_code, indicator_code='SL.UEM.TOTL.ZS')
        if mode == 'ML':
            return data['value']
        if mode == 'F':
            return data['value'].iloc[0]

    @feature(
            name='youth_unemployment',
            group='economic_features',
            deps=['world_bank:SL.UEM.1524.ZS'],
            compute='youth_unemployment from the World Bank data'
    )    
    def youth_unemployment(self, country_code: str, mode: str = Literal['ML', 'F']) -> float:
        check_iso3(code=country_code)
        data = self.wb.fetch(country_code=country_code, indicator_code='SL.UEM.1524.ZS')
        if mode == 'ML':
            return data['value']
        if mode == 'F':
            return data['value'].iloc[0]

    @feature(
            name='labor_force_participation',
            group='economic_features',
            deps=['world_bank:SL.TLF.CACT.ZS'],
            compute='labor_force_participation from the World Bank data'
    )    
    def labor_force_participation(self, country_code: str, mode: str = Literal['ML', 'F']) -> float:
        check_iso3(code=country_code)
        data = self.wb.fetch(country_code=country_code, indicator_code='SL.TLF.CACT.ZS')
        if mode == 'F':
            return data['value'].iloc[0]
        if mode == 'ML':
            return data['value']

    @feature(
            name='current_account_gdp_ratio',
            group='economic_features',
            deps=['world_bank:BN.CAB.XOKA.GD.ZS'],
            compute='current_account_gdp_ratio from the World Bank data'
    )    
    def current_account_gdp_ratio(self, country_code: str, mode: str = Literal['ML', 'F']) -> float:
        check_iso3(code=country_code)
        data = self.wb.fetch(country_code=country_code, indicator_code='BN.CAB.XOKA.GD.ZS')
        if mode == 'F':
            return data['value'].iloc[0]
        if mode == 'ML':
            return data['value']

    @feature(
            name='fx_reserves_months_import',
            group='economic_features',
            deps=['world_bank:FI.RES.TOTL.MO'],
            compute='fx_reserves_months_import from the World Bank data'
    )    
    def fx_reserves_months_import(self ,country_code: str, mode: str = Literal['F', 'ML']) -> float:
        check_iso3(code=country_code)
        data = self.wb.fetch(country_code=country_code, indicator_code='FI.RES.TOTL.MO')
        if mode == 'F':
            return data['value'].iloc[0]
        if mode == 'ML':
            return data['value']


    @feature(
            name='external_debt_gdp_ratio',
            group='economic_features',
            deps=['world_bank:DT.DOD.DECT.GN.ZS'],
            compute='external_debt_gdp_ratio from the World Bank data'
    )    
    def external_debt_gdp_ratio(self, country_code: str, mode: str = Literal['ML', 'F']) -> float:
        check_iso3(code=country_code)
        data = self.wb.fetch(country_code=country_code, indicator_code='DT.DOD.DECT.GN.ZS')
        if mode == 'F':
            return data['value'].iloc[0]
        if mode == 'ML':
            return data['value']

    @feature(
            name='fiscal_deficit_gdp',
            group='economic_features',
            deps=['IMF:IMF.RES:WEO:GGXCNL_NGDP'],
            compute='fiscal_deficit_gdp from the IMF data'
    )    
    def fiscal_deficit_gdp(self, country_code: str, mode: str = Literal['ML', 'F']) -> float:
        check_iso3(code=country_code)
        data = self.imf.fetch(country=country_code, agency='IMF.RES', dataflow_id='WEO', key='GGXCNL_NGDP')
        if mode == 'F':
            return data['value'].iloc[0]
        if mode == 'ML':
            return data['value']

    @feature(
            name='government_debt_gdp',
            group='economic_features',
            deps=['IMF:IMF.RES:WEO:GGXWDG_NGDP'],
            compute='government_debt_gdp from the IMF data'
    )    
    def government_debt_gdp(self, country_code: str, mode: str = Literal['ML', 'F']) -> float:
        check_iso3(code=country_code)
        data = self.imf.fetch(country=country_code, agency='IMF.RES', dataflow_id='WEO', key='GGXWDG_NGDP')
        if mode == 'F':
            return data['value'].iloc[0]
        if mode == 'ML':
            return data['value']

    @feature(
            name='reer_misalignment',
            group='economic_features',
            deps=['IMF:IMF.STA:IFS:EREER_IX.M'],
            compute='reer_misalignment from the IMF data'
    )    
    def reer_misalignment(self, country_code: str, mode: str = Literal['ML', 'F']) -> float:
        check_iso3(code=country_code)
        data = self.imf.fetch(country=country_code, agency='IMF.STA', dataflow_id='IFS', key='EREER_IX.M')
        if mode == 'F':
            return data['value'].iloc[0]
        if mode == 'ML':
            return data['value']

        
    @feature(
            name='inflation_yoy',
            group='economic_features',
            deps=['IMF:IMF.STA:CPI:CPI._T.IX.M'],
            compute='inflation_yoy from the IMF data'
    )    
    def inflation_yoy(self, country_code: str, mode: str = Literal['ML', 'F']) -> float:
        check_iso3(code=country_code)
        data = self.imf.fetch(country=country_code, agency='IMF.STA', dataflow_id='CPI', key='CPI._T.IX.M')
        if mode == 'F':
            return data['value'].iloc[0]
        if mode == 'ML':
            return data['value']

    @feature(
            name='banking_sector_health',
            group='economic_features',
            deps=['world_bank:FB.AST.NPLN.ZS'],
            compute='banking_sector_health from the World Bank data'
    )    
    def banking_sector_health(self, country_code: str, mode: str = Literal['ML', 'F']) -> float:
        check_iso3(code=country_code)
        data = self.wb.fetch(country_code=country_code, indicator_code='FB.AST.NPLN.ZS')
        if mode == 'F':
            return data['value'].iloc[0]
        if mode == 'ML':
            return data['value']

    @feature(
            name='gdp_per_capita_ppp',
            group='economic_features',
            deps=['world_bank:NY.GDP.PCAP.PP.CD'],
            compute='gdp_per_capita_ppp from the World Bank data'
    )    
    def gdp_per_capita_ppp(self, country_code: str, mode: str = Literal['ML', 'F']) -> float:
        check_iso3(code=country_code)
        data = self.wb.fetch(country_code=country_code, indicator_code='NY.GDP.PCAP.PP.CD')
        if mode == 'F':
            return data['value'].iloc[0]
        if mode == 'ML':
            return data['value']


