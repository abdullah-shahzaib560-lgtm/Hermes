from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest

from hermes.core.cache import RawCache


@pytest.fixture
def tmp_cache(tmp_path: Path) -> RawCache:
    return RawCache(cache_dir=str(tmp_path / "hermes_cache"))


@pytest.fixture
def sample_wb_df() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "date": ["2023", "2022", "2021"],
            "indicator_id": ["NY.GDP.MKTP.KD.ZG"] * 3,
            "indicator_name": ["GDP growth (annual %)"] * 3,
            "country": ["USA"] * 3,
            "value": [2.5, 1.9, 5.8],
            "source": ["World_Bank"] * 3,
        }
    )


@pytest.fixture
def sample_wb_cpi_df() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "date": ["2023", "2022", "2021"],
            "indicator_id": ["FP.CPI.TOTL"] * 3,
            "indicator_name": ["Consumer price index"] * 3,
            "country": ["USA"] * 3,
            "value": [120.5, 117.8, 115.2],
            "source": ["World_Bank"] * 3,
        }
    )


@pytest.fixture
def sample_imf_df() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "date": ["2023", "2022", "2021"],
            "indicator_id": ["PPI.IX.A"] * 3,
            "indicator_name": ["Producer price index"] * 3,
            "country": ["USA"] * 3,
            "value": [110.0, 107.5, 105.0],
            "source": ["IMF"] * 3,
        }
    )
