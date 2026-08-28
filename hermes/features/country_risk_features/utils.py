import logging

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


def check_empty(mode, data, country="unknown"):
    if data.empty:
        logger.warning(f"No Data for {country}")
        return empty_result(mode)

    if "value" in data.columns:
        data = data[data["value"].notna()]

    if data.empty:
        logger.warning(f"No valid data for {country}")
        return empty_result(mode)

    return data


def empty_result(mode: str):
    return np.nan if mode == "F" else pd.Series(dtype=float)


def adjust_year_range(df, year_col, start_year, end_year, fill_method="null", fill_value=0):
    full_years = pd.DataFrame({year_col: range(start_year, end_year + 1)})

    df_filtered = df[(df[year_col] >= start_year) & (df[year_col] <= end_year)]

    adjusted_df = pd.merge(full_years, df_filtered, on=year_col, how="left")

    if fill_method == "value":
        adjusted_df = adjusted_df.fillna(fill_value)
    elif fill_method == "ffill":
        adjusted_df = adjusted_df.ffill().bfill()
    elif fill_method == "bfill":
        adjusted_df = adjusted_df.bfill().ffill()
    elif fill_method == "linear":
        adjusted_df = adjusted_df.interpolate(method="linear").bfill().ffill()

    return adjusted_df


__all__ = ["check_empty", "empty_result", "adjust_year_range"]
