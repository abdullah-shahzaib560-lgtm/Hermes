from pathlib import Path

import pandas as pd

CURRENT_DIR = Path(__file__).parent
CSV_PATH = CURRENT_DIR / "lib" / "datasets" / "hdi1.csv"

class VDEMHDI:
    def __init__(self):
        self._data = pd.read_csv(CSV_PATH)

    def fetch(
        self,
        country: str
    ) -> pd.DataFrame:

        self._data["Year"] = pd.to_datetime(self._data["year"], format="%Y")
        df = self._data[self._data["country"] == country]
        return df

