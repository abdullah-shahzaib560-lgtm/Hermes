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
    def test_fetch_success(self, tmp_cache):
        os = OpenSanction(cache=tmp_cache, api_key="test-key")
        respx.get(f"{OS_URL}/search/default", params={"countries": "US", "limit": 0}).respond(
            status_code=200,
            content=b'{"results": []}',
        )
        os._fetch("USA", facets="", changed_since=None, topics="")
        assert len(respx.calls) == 1

    @respx.mock
    def test_fetch_404(self, tmp_cache):
        os = OpenSanction(cache=tmp_cache, api_key="test-key")
        respx.get(f"{OS_URL}/search/default", params={"countries": "US", "limit": 0}).respond(
            status_code=404,
            content=b"{}",
        )
        df = os._fetch("USA", facets="", changed_since=None, topics="")
        assert df.empty

    @respx.mock
    def test_fetch_http_error(self, tmp_cache):
        os = OpenSanction(cache=tmp_cache, api_key="test-key")
        respx.get(f"{OS_URL}/search/default", params={"countries": "US", "limit": 0}).respond(
            status_code=500,
            content=b"{}",
        )
        with pytest.raises(httpx.HTTPStatusError):
            os._fetch("USA", facets="", changed_since=None, topics="")

    def test_no_dataset_raises(self, tmp_cache):
        os = OpenSanction(cache=tmp_cache, api_key="test-key")
        with pytest.raises(ValueError, match="dataset parameter is empty"):
            os._fetch("USA", facets="", changed_since=None, topics="", dataset="")
