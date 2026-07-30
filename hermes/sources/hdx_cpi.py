from datetime import timedelta
from pathlib import Path

import pandas as pd

from hermes.core.cache import RawCache

CURRENT_DIR = Path(__file__).parent
CSV_PATH = CURRENT_DIR / "lib" / "datasets" / "global_cpi_all.csv"


class HDXCPI:
    def __init__(self, cache: RawCache | None = None):
        self._data = pd.read_csv(CSV_PATH)
        self._cache = cache or RawCache()

    def _fetch(
        self,
        country: str,
    ) -> pd.DataFrame:

        df = self._data[["iso3", "year", "score"]]
        df["year"] = pd.to_datetime(df["year"], format="%Y")
        df = df[df["iso3"] == country]
        return df

    def fetch(self, country: str, force: bool = False) -> pd.DataFrame:

        cached_params = {"country": country}

        return self._cache.get_or_fetch(
            source="HDX_CPI",
            params=cached_params,
            fetch_fn=lambda: self._fetch(country=country),
            force=force,
            ttl=timedelta(minutes=60),
        )


if __name__ == "__main__":
    data = HDXCPI()
