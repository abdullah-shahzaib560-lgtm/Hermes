import logging

import numpy as np
import pandas as pd
import pycountry

logger = logging.getLogger(__name__)


def iso3_to_iso2(iso3_code):
    try:
        return pycountry.countries.get(alpha_3=iso3_code.upper()).alpha_2
    except AttributeError:
        return "Not Found"


def check_iso3(code):
    country = pycountry.countries.get(alpha_3=code.upper())
    if not country:
        raise RuntimeError(f"The {code} is not iso3")


def check_empty(mode, data, country):
    if data.empty:
        logger.warning(f"No Data for {country}")
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
