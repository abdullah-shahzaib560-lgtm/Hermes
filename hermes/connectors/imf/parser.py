import pandas as pd

EMPTY_COLS = ["date", "indicator_id", "country", "value", "source"]


def empty_dataframe() -> pd.DataFrame:
    return pd.DataFrame(columns=EMPTY_COLS)


__all__ = ["EMPTY_COLS", "empty_dataframe"]
