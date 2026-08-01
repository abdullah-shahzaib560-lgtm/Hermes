from pathlib import Path

import pandas as pd

CURRENT_DIR = Path(__file__).parent
CSV_PATH = CURRENT_DIR / "lib" / "datasets" / "global_cpi_all.csv"


class HDXCPI:
    def __init__(self):
        self._data = pd.read_csv(CSV_PATH)

    def fetch(
        self,
        country: str,
    ) -> pd.DataFrame:

        df = self._data[["iso3", "year", "score"]]
        df["year"] = pd.to_datetime(df["year"], format="%Y")
        df = df[df["iso3"] == country]
        return df


if __name__ == "__main__":
    data = HDXCPI()
