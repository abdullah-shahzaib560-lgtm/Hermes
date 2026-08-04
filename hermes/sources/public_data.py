from pathlib import Path

import pandas as pd

CURRENT_DIR = Path(__file__).parent

HRS_PATH = CURRENT_DIR / "lib" / "datasets" / "hrs.csv"
HDI_PATH = CURRENT_DIR / "lib" / "datasets" / "hdi1.csv"
CPI_PATH = CURRENT_DIR / "lib" / "datasets" / "global_cpi_all.csv"
FSI_PATH = CURRENT_DIR / "lib" / "datasets" / "fsi.csv"

class PUBLIC_DATASET:
    def fetch_hrs(self, country: str) -> pd.DataFrame:
        df = pd.read_csv(HRS_PATH)
        data = df[df["country_text_id"] == country]
        data["date"] = pd.to_datetime(data["date"], format="%Y")
        return data

    def fetch_hdi(
        self,
        country: str,
    ) -> pd.DataFrame:
        df = pd.read_csv(HDI_PATH)
        data = df[["iso3", "year", "score"]]
        data["year"] = pd.to_datetime(data["year"], format="%Y")
        data = data[data["iso3"] == country]
        return data

    def fetch_cpi(self, country: str) -> pd.DataFrame:
        df = pd.read_csv(CPI_PATH)
        data = df[["iso3", "year", "score"]]
        data["year"] = pd.to_datetime(data["year"], format="%Y")
        data = data[data["iso3"] == country]
        return data

    def fetch_fsi(self, country: str) -> pd.DataFrame:
        df = pd.read_csv(FSI_PATH)
        data = df[df['country'] == country]
        data['Year'] = pd.to_datetime(data['Year'], format='%Y')
        return data
