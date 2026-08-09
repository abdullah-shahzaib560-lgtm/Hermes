from __future__ import annotations

import httpx
import pytest
import respx

from hermes.core.helper import iso3_to_iso2
from hermes.sources.imf import IMF

IMF_URL = "https://api.imf.org/external/sdmx/3.0/data/dataflow"


@pytest.fixture
def sample_sdmx_response():
    return {
        "data": {
            "structures": [
                {
                    "dimensions": {
                        "series": [
                            {"id": "FREQ", "values": [{"id": "A", "name": "Annual"}]},
                            {"id": "INDICATOR", "values": [{"id": "PPI.IX.A", "name": "PPI"}]},
                            {"id": "COUNTRY", "values": [{"id": "USA", "name": "United States"}]},
                        ],
                        "observation": [
                            {
                                "id": "TIME_PERIOD",
                                "values": [
                                    {"id": "2023", "name": "2023", "value": "2023"},
                                    {"id": "2022", "name": "2022", "value": "2022"},
                                ],
                            },
                        ],
                    }
                }
            ],
            "dataSets": [
                {
                    "series": {
                        "0:0:0": {
                            "observations": {
                                "0": [110.5],
                                "1": [107.2],
                            }
                        }
                    }
                }
            ],
        }
    }


class TestIso3ToIso2:
    def test_valid(self):
        assert iso3_to_iso2("USA") == "US"

    def test_invalid(self):
        assert iso3_to_iso2("ZZZ") == "Not Found"


class TestIMF:
    @respx.mock
    async def test_fetch_success(self, tmp_path, sample_sdmx_response):
        imf = IMF(cache=None)
        url = f"{IMF_URL}/IMF.STA/PPI/~/USA.PPI.IX.A"
        respx.get(url).respond(status_code=200, json=sample_sdmx_response)
        df = await imf._fetch("USA", "IMF.STA", "PPI", "PPI.IX.A")
        assert not df.empty
        assert df["value"].iloc[0] == 110.5
        assert df["country"].iloc[0] == "USA"
        assert df["source"].iloc[0] == "IMF"

    @respx.mock
    async def test_fetch_no_series(self, tmp_path):
        imf = IMF(cache=None)
        url = f"{IMF_URL}/IMF.STA/PPI/~/USA.PPI.IX.A"
        respx.get(url).respond(
            status_code=200,
            json={
                "data": {
                    "structures": [
                        {
                            "dimensions": {
                                "series": [],
                                "observation": [{"id": "TIME_PERIOD", "values": []}],
                            }
                        }
                    ],
                    "dataSets": [{}],
                }
            },
        )
        df = await imf._fetch("USA", "IMF.STA", "PPI", "PPI.IX.A")
        assert df.empty

    @respx.mock
    async def test_fetch_404(self, tmp_path):
        imf = IMF(cache=None)
        url = f"{IMF_URL}/IMF.STA/BAD/~/USA.X"
        respx.get(url).respond(status_code=404)
        df = await imf._fetch("USA", "IMF.STA", "BAD", "X")
        assert df.empty

    @respx.mock
    async def test_fetch_http_error(self, tmp_path):
        imf = IMF(cache=None)
        url = f"{IMF_URL}/IMF.STA/PPI/~/USA.PPI.IX.A"
        respx.get(url).respond(status_code=500)
        with pytest.raises(httpx.HTTPStatusError):
            await imf._fetch("USA", "IMF.STA", "PPI", "PPI.IX.A")
