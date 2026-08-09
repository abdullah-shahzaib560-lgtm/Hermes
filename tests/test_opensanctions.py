from __future__ import annotations

import httpx
import pytest
import respx

from hermes.sources.opensanctions import OpenSanction, iso3_to_iso2

OS_URL = "https://api.opensanctions.org"


class TestIso3ToIso2:
    def test_valid(self):
        assert iso3_to_iso2("USA") == "US"

    def test_invalid(self):
        assert iso3_to_iso2("ZZZ") == "Not Found"


class TestOpenSanction:
    @respx.mock
    async def test_fetch_success(self, tmp_cache):
        os = OpenSanction(cache=tmp_cache, api_key="test-key")
        respx.get(f"{OS_URL}/search/default", params={"countries": "US", "limit": 0}).respond(
            status_code=200,
            content=b'{"results": []}',
        )
        await os.fetch("USA", dataset="default", limit=0)
        assert len(respx.calls) == 1

    @respx.mock
    async def test_fetch_404(self, tmp_cache):
        os = OpenSanction(cache=tmp_cache, api_key="test-key")
        respx.get(f"{OS_URL}/search/default", params={"countries": "US", "limit": 0}).respond(
            status_code=404,
            content=b"{}",
        )
        result = await os.fetch("USA", dataset="default", limit=0)
        assert result == {}

    @respx.mock
    async def test_fetch_http_error(self, tmp_cache):
        os = OpenSanction(cache=tmp_cache, api_key="test-key")
        respx.get(f"{OS_URL}/search/default", params={"countries": "US", "limit": 0}).respond(
            status_code=500,
            content=b"{}",
        )
        with pytest.raises(httpx.HTTPStatusError):
            await os.fetch("USA", dataset="default", limit=0)

    async def test_no_dataset_raises(self, tmp_cache):
        os = OpenSanction(cache=tmp_cache, api_key="test-key")
        with pytest.raises(ValueError, match="dataset parameter is empty"):
            await os.fetch("USA", dataset="", limit=0)
