import logging
from typing import Literal

import pandas as pd

from hermes.core.feature_decorator import feature
from hermes.core.helper import check_empty
from hermes.sources.imf import IMF
from hermes.sources.world_bank import World_bank

logger = logging.getLogger(__name__)


class economic_features:
    def __init__(self):
        self.wb = World_bank()
        self.imf = IMF()

    @feature(
        name="gdp_growth_yoy",
        group="economic_features",
        deps=["world_bank:NY.GDP.MKTP.KD.ZG"],
        compute="GDP growth YoY, merged from WB and IMF",
    )
    def gdp_growth_yoy(self, country_code: str, mode: str = Literal["ML", "F"]) -> float | pd.Series:
        data = self.wb.fetch(country_code=country_code, indicator_code="NY.GDP.MKTP.KD.ZG")
        data = check_empty(mode=mode, data=data, country=country_code)
        return data

    @feature(
        name="gdp_growth_qoq",
        group="economic_features",
        deps=["world_bank:NY.GDP.MKTP.KD"],
        compute="GDP growth QoQ, interpolated from the annual frequency data from the World_Bank",
    )
    def gdp_growth_qoq(self, country_code: str, mode: str = Literal["ML", "F"]) -> float | pd.Series:
        data = self.wb.fetch(country_code=country_code, indicator_code="NY.GDP.MKTP.KD")

        data = check_empty(mode=mode, country=country_code, data=data)
        if not isinstance(data, pd.DataFrame):
            return data

        data["date"] = pd.to_datetime(data["date"].astype(str) + "-12-31")
        data = data.set_index("date")
        df = data[["value"]].resample("QE").interpolate(method="linear")
        df["gdp_growth_qoq"] = df["value"].pct_change() * 100

        if mode == "F":
            return df["gdp_growth_qoq"].iloc[0]
        if mode == "ML":
            df["value"] = df["gdp_growth_qoq"].resample("MS").interpolate()
            return df["value"]

    @feature(
        name="industrial_production_yoy",
        group="economic_features",
        deps=["world_bank:NV.IND.MANF.KD.ZG"],
        compute="industrial_production_yoy from the World Bank data",
    )
    def industrial_production_yoy(self, country_code: str, mode: str = Literal["ML", "F"]) -> float | pd.Series:
        data = self.wb.fetch(country_code=country_code, indicator_code="NV.IND.MANF.KD.ZG")

        data = check_empty(mode=mode, country=country_code, data=data)
        if not isinstance(data, pd.DataFrame):
            return data

        if mode == "F":
            return float(data["value"].iloc[0])

        if mode == "ML":
            data = data.set_index("date")
            data.index = pd.to_datetime(data.index)
            data = data.sort_index()
            data = data.resample("MS").ffill()
            return data["value"]

    @feature(
        name="inflation_cpi_yoy",
        group="economic_features",
        deps=["world_bank:FP.CPI.TOTL.ZG"],
        compute="inflation_cpi_yoy from the World Bank data",
    )
    def inflation_cpi_yoy(self, country_code: str, mode: str = Literal["ML", "F"]) -> float | pd.Series:
        data = self.wb.fetch(country_code=country_code, indicator_code="FP.CPI.TOTL.ZG")

        data = check_empty(mode=mode, country=country_code, data=data)
        if not isinstance(data, pd.DataFrame):
            return data

        if mode == "F":
            return float(data["value"].iloc[0])

        if mode == "ML":
            data = data.set_index("date")
            data.index = pd.to_datetime(data.index)
            data = data.sort_index()
            data = data.resample("MS").interpolate()
            return data["value"]

    @feature(
        name="inflation_volatility_12m",
        group="economic_features",
        deps=["world_bank:FP.CPI.TOTL"],
        compute="inflation_volatility_12m from the World Bank data",
    )
    def inflation_volatility_12m(self, country_code: str, mode: str = Literal["ML", "F"]) -> float | pd.Series:
        data = self.wb.fetch(country_code=country_code, indicator_code="FP.CPI.TOTL")

        data = check_empty(mode=mode, country=country_code, data=data)
        if not isinstance(data, pd.DataFrame):
            return data

        data["date"] = pd.to_datetime(data["date"].astype(str) + "-12-31")
        data = data.sort_values("date").set_index("date")

        monthly = data[["value"]].resample("MS").interpolate(method="linear")
        monthly["yoy_change"] = monthly["value"].pct_change(12)
        monthly["inflation_volatility_12m"] = monthly["yoy_change"].rolling(12).std()

        result = monthly["inflation_volatility_12m"].dropna().sort_index(ascending=False)

        if mode == "F":
            return result.iloc[0]
        if mode == "ML":
            return result

    @feature(
        name="ppi_yoy",
        group="economic_features",
        deps=["IMF:IMF.STA:PPI:PPI.IX.A"],
        compute="ppi_yoy from the IMF data",
    )
    def ppi_yoy(self, country_code: str, mode: str = Literal["ML", "F"]) -> float | pd.Series:
        data = self.imf.fetch(country=country_code, agency="IMF.STA", dataflow_id="PPI", key="PPI.IX.A")

        data = check_empty(mode=mode, country=country_code, data=data)
        if not isinstance(data, pd.DataFrame):
            return data

        if mode == "F":
            return data["value"].iloc[0]
        if mode == "ML":
            data = data.set_index("date")
            data.index = pd.to_datetime(data.index)
            data.sort_index(inplace=True)
            data = data.resample("MS").interpolate()
            return data["value"]

    @feature(
        name="inflation_yoy",
        group="economic_features",
        deps=["world_bank:NV.IND.MANF.KD.ZG"],
        compute="inflation_yoy from the IMF data",
    )
    def inflation_yoy(self, country_code: str, mode: str = Literal["ML", "F"]) -> float | pd.Series:
        data = self.imf.fetch(country=country_code, agency="IMF.STA", dataflow_id="CPI", key="CPI._T.IX.M")

        data = check_empty(mode=mode, country=country_code, data=data)
        if not isinstance(data, pd.DataFrame):
            return data

        if mode == "F":
            return data["value"].iloc[0]
        if mode == "ML":
            data = data.set_index("date")
            data.index = pd.to_datetime(data.index)
            data.sort_index(inplace=True)
            data = data.resample("MS").interpolate()
            return data["value"]

    @feature(
        name="unemployment_rate",
        group="economic_features",
        deps=["world_bank:SL.UEM.TOTL.ZS"],
        compute="unemployment_rate from the World Bank data",
    )
    def unemployment_rate(self, country_code: str, mode: str = Literal["ML", "F"]) -> float | pd.Series:
        data = self.wb.fetch(country_code=country_code, indicator_code="SL.UEM.TOTL.ZS")

        data = check_empty(mode=mode, country=country_code, data=data)
        if not isinstance(data, pd.DataFrame):
            return data

        if mode == "F":
            return data["value"].iloc[0]
        if mode == "ML":
            data = data.set_index("date")
            data.index = pd.to_datetime(data.index)
            data.sort_index(inplace=True)
            data = data.resample("MS").interpolate()
            return data["value"]

    @feature(
        name="youth_unemployment",
        group="economic_features",
        deps=["world_bank:SL.UEM.1524.ZS"],
        compute="youth_unemployment from the World Bank data",
    )
    def youth_unemployment(self, country_code: str, mode: str = Literal["ML", "F"]) -> float | pd.Series:
        data = self.wb.fetch(country_code=country_code, indicator_code="SL.UEM.1524.ZS")

        data = check_empty(mode=mode, country=country_code, data=data)
        if not isinstance(data, pd.DataFrame):
            return data

        if mode == "F":
            return data["value"].iloc[0]
        if mode == "ML":
            data = data.set_index("date")
            data.index = pd.to_datetime(data.index)
            data.sort_index(inplace=True)
            data = data.resample("MS").interpolate()
            return data["value"]

    @feature(
        name="labor_force_participation",
        group="economic_features",
        deps=["world_bank:SL.TLF.CACT.ZS"],
        compute="labor_force_participation from the World Bank data",
    )
    def labor_force_participation(self, country_code: str, mode: str = Literal["ML", "F"]) -> float | pd.Series:
        data = self.wb.fetch(country_code=country_code, indicator_code="SL.TLF.CACT.ZS")

        data = check_empty(mode=mode, country=country_code, data=data)
        if not isinstance(data, pd.DataFrame):
            return data

        if mode == "F":
            return data["value"].iloc[0]
        if mode == "ML":
            data = data.set_index("date")
            data.index = pd.to_datetime(data.index)
            data.sort_index(inplace=True)
            data = data.resample("MS").interpolate()
            return data["value"]

    @feature(
        name="current_account_gdp_ratio",
        group="economic_features",
        deps=["world_bank:BN.CAB.XOKA.GD.ZS"],
        compute="current_account_gdp_ratio from the World Bank data",
    )
    def current_account_gdp_ratio(self, country_code: str, mode: str = Literal["ML", "F"]) -> float | pd.Series:
        data = self.wb.fetch(country_code=country_code, indicator_code="BN.CAB.XOKA.GD.ZS")

        data = check_empty(mode=mode, country=country_code, data=data)
        if not isinstance(data, pd.DataFrame):
            return data

        if mode == "F":
            return data["value"].iloc[0]
        if mode == "ML":
            data = data.set_index("date")
            data.index = pd.to_datetime(data.index)
            data.sort_index(inplace=True)
            data = data.resample("MS").interpolate()
            return data["value"]

    @feature(
        name="fx_reserves_months_import",
        group="economic_features",
        deps=["world_bank:FI.RES.TOTL.MO"],
        compute="fx_reserves_months_import from the World Bank data",
    )
    def fx_reserves_months_import(self, country_code: str, mode: str = Literal["F", "ML"]) -> float | pd.Series:
        data = self.wb.fetch(country_code=country_code, indicator_code="FI.RES.TOTL.MO")

        data = check_empty(mode=mode, country=country_code, data=data)
        if not isinstance(data, pd.DataFrame):
            return data

        if mode == "F":
            return data["value"].iloc[0]
        if mode == "ML":
            data = data.set_index("date")
            data.index = pd.to_datetime(data.index)
            data.sort_index(inplace=True)
            data = data.resample("MS").interpolate()
            return data["value"]

    @feature(
        name="external_debt_gdp_ratio",
        group="economic_features",
        deps=["world_bank:DT.DOD.DECT.GN.ZS"],
        compute="external_debt_gdp_ratio from the World Bank data",
    )
    def external_debt_gdp_ratio(self, country_code: str, mode: str = Literal["ML", "F"]) -> float | pd.Series:
        data = self.wb.fetch(country_code=country_code, indicator_code="DT.DOD.DECT.GN.ZS")

        data = check_empty(mode=mode, country=country_code, data=data)
        if not isinstance(data, pd.DataFrame):
            return data

        if mode == "F":
            return data["value"].iloc[0]
        if mode == "ML":
            data = data.set_index("date")
            data.index = pd.to_datetime(data.index)
            data.sort_index(inplace=True)
            data = data.resample("MS").interpolate()
            return data["value"]

    @feature(
        name="fiscal_deficit_gdp",
        group="economic_features",
        deps=["IMF:IMF.RES:WEO:GGXCNL_NGDP"],
        compute="fiscal_deficit_gdp from the IMF data",
    )
    def fiscal_deficit_gdp(self, country_code: str, mode: str = Literal["ML", "F"]) -> float | pd.Series:
        data = self.imf.fetch(country=country_code, agency="IMF.RES", dataflow_id="WEO", key="GGXCNL_NGDP")

        data = check_empty(mode=mode, country=country_code, data=data)
        if not isinstance(data, pd.DataFrame):
            return data

        if mode == "F":
            return data["value"].iloc[0]
        if mode == "ML":
            data = data.set_index("date")
            data.index = pd.to_datetime(data.index)
            data.sort_index(inplace=True)
            data = data.resample("MS").interpolate()
            return data["value"]

    @feature(
        name="government_debt_gdp",
        group="economic_features",
        deps=["IMF:IMF.RES:WEO:GGXWDG_NGDP"],
        compute="government_debt_gdp from the IMF data",
    )
    def government_debt_gdp(self, country_code: str, mode: str = Literal["ML", "F"]) -> float | pd.Series:
        data = self.imf.fetch(country=country_code, agency="IMF.RES", dataflow_id="WEO", key="GGXWDG_NGDP")

        data = check_empty(mode=mode, country=country_code, data=data)
        if not isinstance(data, pd.DataFrame):
            return data

        if mode == "F":
            return data["value"].iloc[0]
        if mode == "ML":
            data = data.set_index("date")
            data.index = pd.to_datetime(data.index)
            data.sort_index(inplace=True)
            data = data.resample("MS").interpolate()
            return data["value"]

    @feature(
        name="reer_misalignment",
        group="economic_features",
        deps=["IMF:IMF.STA:ER:EREER_IX.M"],
        compute="reer_misalignment from the IMF data",
    )
    def reer_misalignment(self, country_code: str, mode: str = Literal["ML", "F"]) -> float | pd.Series:
        data = self.imf.fetch(country=country_code, agency="IMF.STA", dataflow_id="ER", key="EREER_IX.M")

        data = check_empty(mode=mode, country=country_code, data=data)
        if not isinstance(data, pd.DataFrame):
            return data

        if mode == "F":
            return data["value"].iloc[0]
        if mode == "ML":
            data = data.set_index("date")
            data.index = pd.to_datetime(data.index)
            data.sort_index(inplace=True)
            data = data.resample("MS").interpolate()
            return data["value"]

    @feature(
        name="banking_sector_health",
        group="economic_features",
        deps=["world_bank:FB.AST.NPLN.ZS"],
        compute="banking_sector_health from the World Bank data",
    )
    def banking_sector_health(self, country_code: str, mode: str = Literal["ML", "F"]) -> float | pd.Series:
        data = self.wb.fetch(country_code=country_code, indicator_code="FB.AST.NPLN.ZS")

        data = check_empty(mode=mode, country=country_code, data=data)
        if not isinstance(data, pd.DataFrame):
            return data

        if mode == "F":
            return data["value"].iloc[0]
        if mode == "ML":
            data = data.set_index("date")
            data.index = pd.to_datetime(data.index)
            data.sort_index(inplace=True)
            data = data.resample("MS").interpolate()
            return data["value"]

    @feature(
        name="gdp_per_capita_ppp",
        group="economic_features",
        deps=["world_bank:NY.GDP.PCAP.PP.CD"],
        compute="gdp_per_capita_ppp from the World Bank data",
    )
    def gdp_per_capita_ppp(self, country_code: str, mode: str = Literal["ML", "F"]) -> float | pd.Series:
        data = self.wb.fetch(country_code=country_code, indicator_code="NY.GDP.PCAP.PP.CD")

        data = check_empty(mode=mode, country=country_code, data=data)
        if not isinstance(data, pd.DataFrame):
            return data

        if mode == "F":
            return data["value"].iloc[0]
        if mode == "ML":
            data = data.set_index("date")
            data.index = pd.to_datetime(data.index)
            data.sort_index(inplace=True)
            data = data.resample("MS").interpolate()
            return data["value"]


if __name__ == "__main__":
    eco = economic_features()
    wb = World_bank()
    data = eco.inflation_volatility_12m("USA", "ML")
    data.to_csv("data/data.csv")
    print(data)
