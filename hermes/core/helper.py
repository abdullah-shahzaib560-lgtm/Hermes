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
