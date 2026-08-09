from __future__ import annotations

import httpx
import pytest
import respx

from hermes.sources.world_bank import World_bank

WB_API_URL = "https://api.worldbank.org/v2"


class TestWorldBank:
    @respx.mock
    async def test_fetch_success(self, tmp_path):
        wb = World_bank(cache=None)
        respx.get(f"{WB_API_URL}/country/USA/indicator/NY.GDP.MKTP.KD.ZG").respond(
            status_code=200,
            json=[
                {"page": 1, "pages": 1, "per_page": 1000, "total": 1},
                [
                    {
                        "indicator": {"id": "NY.GDP.MKTP.KD.ZG", "value": "GDP growth"},
                        "countryiso3code": "USA",
                        "date": "2023",
                        "value": 2.5,
                    }
                ],
            ],
        )
        df = await wb._fetch("USA", "NY.GDP.MKTP.KD.ZG")
        assert not df.empty
        assert df["value"].iloc[0] == 2.5
        assert df["country"].iloc[0] == "USA"
        assert df["source"].iloc[0] == "World_Bank"

    @respx.mock
    async def test_fetch_no_data(self, tmp_path):
        wb = World_bank(cache=None)
        respx.get(f"{WB_API_URL}/country/XYZ/indicator/SOME.IND").respond(
            status_code=200,
            json=[{"page": 1, "pages": 1}, []],
        )
        df = await wb._fetch("XYZ", "SOME.IND")
        assert df.empty

    @respx.mock
    async def test_fetch_http_error(self, tmp_path):
        wb = World_bank(cache=None)
        respx.get(f"{WB_API_URL}/country/USA/indicator/BAD").respond(status_code=404)
        with pytest.raises(httpx.HTTPStatusError):
            await wb._fetch("USA", "BAD")

    @respx.mock
    async def test_fetch_retry_on_timeout(self, tmp_path):
        wb = World_bank(cache=None)
        route = respx.get(f"{WB_API_URL}/country/USA/indicator/NY.GDP.MKTP.KD.ZG")
        route.mock(side_effect=httpx.ReadTimeout("timed out"))

        with pytest.raises(httpx.ReadTimeout):
            await wb._fetch("USA", "NY.GDP.MKTP.KD.ZG", retries=1)

    @respx.mock
    async def test_public_fetch_uses_cache(self, tmp_cache, tmp_path):
        wb = World_bank(cache=tmp_cache)
        respx.get(f"{WB_API_URL}/country/USA/indicator/GDP.PROT").respond(
            status_code=200,
            json=[
                {"page": 1, "pages": 1, "per_page": 1000, "total": 1},
                [
                    {
                        "indicator": {"id": "GDP.PROT", "value": "Test"},
                        "countryiso3code": "USA",
                        "date": "2023",
                        "value": 3.0,
                    }
                ],
            ],
        )
        df1 = await wb.fetch("USA", "GDP.PROT")
        df2 = await wb.fetch("USA", "GDP.PROT")
        assert len(respx.calls) == 1
        assert not df1.empty
        assert not df2.empty
