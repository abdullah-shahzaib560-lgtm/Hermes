from __future__ import annotations

from unittest.mock import MagicMock

import numpy as np
import pandas as pd
import pytest

from hermes.core.helper import check_empty, check_iso3, empty_result, iso3_to_iso2
from hermes.features.country_risk_features.economic import economic_features


class TestHelpers:
    def test_check_iso3_valid(self):
        check_iso3("USA")

    def test_check_iso3_invalid(self):
        with pytest.raises(RuntimeError, match="not iso3"):
            check_iso3("ZZZ")

    def test_empty_result_F(self):
        assert np.isnan(empty_result("F"))

    def test_empty_result_ML(self):
        result = empty_result("ML")
        assert isinstance(result, pd.Series)
        assert result.dtype == float

    def test_check_empty_F(self):
        data = pd.DataFrame({"value": [1.0]})
        result = check_empty("F", data, "USA")
        assert not result.empty

    def test_check_empty_empty(self):
        data = pd.DataFrame()
        result = check_empty("F", data, "USA")
        assert np.isnan(result)


class TestEconomicFeatures:
    @pytest.fixture
    def eco(self):
        return economic_features()

    @pytest.fixture
    def mock_wb(self, eco, sample_wb_df):
        eco.wb = MagicMock()
        eco.wb.fetch.return_value = sample_wb_df
        return eco.wb

    @pytest.fixture
    def mock_wb_cpi(self, eco, sample_wb_cpi_df):
        eco.wb = MagicMock()
        eco.wb.fetch.return_value = sample_wb_cpi_df
        return eco.wb

    @pytest.fixture
    def mock_imf(self, eco, sample_imf_df):
        eco.imf = MagicMock()
        eco.imf.fetch.return_value = sample_imf_df
        return eco.imf

    def test_gdp_growth_yoy_F(self, eco, mock_wb):
        result = eco.gdp_growth_yoy("USA", mode="F")
        assert not result.empty
        assert result["value"].iloc[0] == 2.5

    def test_gdp_growth_yoy_ML(self, eco, mock_wb):
        result = eco.gdp_growth_yoy("USA", mode="ML")
        assert isinstance(result, pd.DataFrame)

    def test_gdp_growth_yoy_empty(self, eco):
        eco.wb = MagicMock()
        eco.wb.fetch.return_value = pd.DataFrame()
        val = eco.gdp_growth_yoy("USA", mode="F")
        assert np.isnan(val)

    def test_gdp_growth_qoq_F(self, eco, mock_wb):
        val = eco.gdp_growth_qoq("USA", mode="F")
        assert isinstance(val, float)

    def test_gdp_growth_qoq_empty(self, eco):
        eco.wb = MagicMock()
        eco.wb.fetch.return_value = pd.DataFrame()
        val = eco.gdp_growth_qoq("USA", mode="F")
        assert np.isnan(val)

    def test_industrial_production_yoy_F(self, eco, mock_wb):
        val = eco.industrial_production_yoy("USA", mode="F")
        assert val == 2.5

    def test_industrial_production_yoy_empty_F(self, eco):
        eco.wb = MagicMock()
        eco.wb.fetch.return_value = pd.DataFrame()
        val = eco.industrial_production_yoy("USA", mode="F")
        assert np.isnan(val)

    def test_inflation_cpi_yoy_F(self, eco, mock_wb):
        val = eco.inflation_cpi_yoy("USA", mode="F")
        assert val == 2.5

    def test_inflation_volatility_12m_F(self, eco, mock_wb_cpi):
        val = eco.inflation_volatility_12m("USA", mode="F")
        assert isinstance(val, float)

    def test_inflation_volatility_12m_empty(self, eco):
        eco.wb = MagicMock()
        eco.wb.fetch.return_value = pd.DataFrame()
        val = eco.inflation_volatility_12m("USA", mode="F")
        assert np.isnan(val)

    def test_ppi_yoy_F(self, eco, mock_imf):
        val = eco.ppi_yoy("USA", mode="F")
        assert val == 110.0

    def test_inflation_yoy_F(self, eco, mock_imf):
        val = eco.inflation_yoy("USA", mode="F")
        assert val == 110.0

    def test_unemployment_rate_F(self, eco, mock_wb):
        val = eco.unemployment_rate("USA", mode="F")
        assert val == 2.5

    def test_youth_unemployment_F(self, eco, mock_wb):
        val = eco.youth_unemployment("USA", mode="F")
        assert val == 2.5

    def test_labor_force_participation_F(self, eco, mock_wb):
        val = eco.labor_force_participation("USA", mode="F")
        assert val == 2.5

    def test_current_account_gdp_ratio_F(self, eco, mock_wb):
        val = eco.current_account_gdp_ratio("USA", mode="F")
        assert val == 2.5

    def test_fx_reserves_months_import_F(self, eco, mock_wb):
        val = eco.fx_reserves_months_import("USA", mode="F")
        assert val == 2.5

    def test_external_debt_gdp_ratio_F(self, eco, mock_wb):
        val = eco.external_debt_gdp_ratio("USA", mode="F")
        assert val == 2.5

    def test_fiscal_deficit_gdp_F(self, eco, mock_imf):
        val = eco.fiscal_deficit_gdp("USA", mode="F")
        assert val == 110.0

    def test_government_debt_gdp_F(self, eco, mock_imf):
        val = eco.government_debt_gdp("USA", mode="F")
        assert val == 110.0

    def test_reer_misalignment_F(self, eco, mock_imf):
        val = eco.reer_misalignment("USA", mode="F")
        assert val == 110.0

    def test_banking_sector_health_F(self, eco, mock_wb):
        val = eco.banking_sector_health("USA", mode="F")
        assert val == 2.5

    def test_gdp_per_capita_ppp_F(self, eco, mock_wb):
        val = eco.gdp_per_capita_ppp("USA", mode="F")
        assert val == 2.5
