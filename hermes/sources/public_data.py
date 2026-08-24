import asyncio
from pathlib import Path

import pandas as pd

CURRENT_DIR = Path(__file__).parent

HRS_PATH = CURRENT_DIR / "lib" / "datasets" / "hrs.csv"
HDI_PATH = CURRENT_DIR / "lib" / "datasets" / "hdi1.csv"
CPI_PATH = CURRENT_DIR / "lib" / "datasets" / "global_cpi_all.csv"
FSI_PATH = CURRENT_DIR / "lib" / "datasets" / "fsi.csv"
NATO_PATH = CURRENT_DIR / "lib" / "datasets" / "nato.csv"
CRS_PATH = CURRENT_DIR / "lib" / "datasets" / "crs.csv"
CVS_PATH = CURRENT_DIR / "lib" / "datasets" / "cvs.csv"
SIPRI_PATH = CURRENT_DIR / "lib" / "datasets" / "sipri.csv"


class PUBLIC_DATASET:
    async def fetch_hrs(self, country: str) -> pd.DataFrame:
        df = await asyncio.to_thread(pd.read_csv, HRS_PATH)
        data = df[df["country"] == country]
        data["date"] = pd.to_datetime(data["date"], format="%Y")
        return data

    async def fetch_hdi(self, country: str) -> pd.DataFrame:
        df = await asyncio.to_thread(pd.read_csv, HDI_PATH)
        df.columns = [c if c != "" else "index" for c in df.columns]
        data = df[["country", "Year", "HDI"]].copy()
        data.columns = ["iso3", "year", "score"]
        data["year"] = pd.to_datetime(data["year"], format="%Y")
        data = data[data["iso3"] == country]
        return data

    async def fetch_cpi(self, country: str) -> pd.DataFrame:
        df = await asyncio.to_thread(pd.read_csv, CPI_PATH)
        data = df[["iso3", "year", "score"]]
        data["year"] = pd.to_datetime(data["year"], format="%Y")
        data = data[data["iso3"] == country]
        return data

    async def fetch_fsi(self, country: str) -> pd.DataFrame:
        df = await asyncio.to_thread(pd.read_csv, FSI_PATH)
        data = df[df["country"] == country].copy()
        data["date"] = pd.to_datetime(data["date"], format="%Y")
        return data

    async def fetch_nato(self, country: str) -> pd.DataFrame:
        df = await asyncio.to_thread(pd.read_csv, NATO_PATH)
        data = df[df["ISO3"] == country]
        data["Year"] = pd.to_datetime(data["Year"], format="%Y")
        return data

    async def fetch_crs(self, country: str) -> pd.DataFrame:
        df = await asyncio.to_thread(pd.read_csv, CRS_PATH)
        data = df[df["ISO3"] == country]
        data["year"] = pd.to_datetime(data["year"], format="%Y")
        return data

    async def fetch_cvs(self, country: str) -> pd.DataFrame:
        df = await asyncio.to_thread(pd.read_csv, CVS_PATH)
        data = df[df["ISO3"] == country]
        data["year"] = pd.to_datetime(data["year"], format="%Y")
        return data

    async def fetch_sipri(self, country: str) -> pd.DataFrame:
        df = await asyncio.to_thread(pd.read_csv, SIPRI_PATH)
        data = df[df["iso3"] == country]
        data["year"] = pd.to_datetime(data["year"], format="%Y")
        return data
