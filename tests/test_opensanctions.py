from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import aiohttp
import pytest

from hermes.sources.opensanctions import OpenSanction, iso3_to_iso2


def _mock_aiohttp_response(json_data, status=200):
    """Create a mock aiohttp response."""
    mock_resp = AsyncMock()
    mock_resp.status = status
    mock_resp.json = AsyncMock(return_value=json_data)
    mock_resp.raise_for_status = MagicMock()

    if status >= 400:
        mock_resp.raise_for_status.side_effect = aiohttp.ClientResponseError(
            request_info=MagicMock(),
            history=(),
            status=status,
        )
    return mock_resp


def _mock_session(mock_resp):
    """Create a mock aiohttp ClientSession that returns the given response."""
    mock_session = AsyncMock()
    mock_session.get = AsyncMock(return_value=mock_resp)
    mock_session.__aenter__ = AsyncMock(return_value=mock_session)
    mock_session.__aexit__ = AsyncMock(return_value=False)
    return mock_session


class TestIso3ToIso2:
    def test_valid(self):
        assert iso3_to_iso2("USA") == "US"

    def test_invalid(self):
        assert iso3_to_iso2("ZZZ") == "Not Found"


class TestOpenSanction:
    async def test_fetch_success(self, tmp_cache):
        os = OpenSanction(cache=tmp_cache, api_key="test-key")
        mock_resp = _mock_aiohttp_response({"results": []})
        mock_session = _mock_session(mock_resp)

        with patch("hermes.sources.opensanctions.aiohttp.ClientSession", return_value=mock_session):
            await os.fetch("USA", dataset="default", limit=0)
            assert mock_session.get.call_count == 1

    async def test_fetch_404(self, tmp_cache):
        os = OpenSanction(cache=tmp_cache, api_key="test-key")
        mock_resp = _mock_aiohttp_response({}, status=404)
        mock_session = _mock_session(mock_resp)

        with patch("hermes.sources.opensanctions.aiohttp.ClientSession", return_value=mock_session):
            result = await os.fetch("USA", dataset="default", limit=0)
            assert result == {}

    async def test_fetch_http_error(self, tmp_cache):
        os = OpenSanction(cache=tmp_cache, api_key="test-key")
        mock_resp = _mock_aiohttp_response({}, status=500)
        mock_session = _mock_session(mock_resp)

        with patch("hermes.sources.opensanctions.aiohttp.ClientSession", return_value=mock_session):
            with pytest.raises(aiohttp.ClientResponseError):
                await os.fetch("USA", dataset="default", limit=0)

    async def test_no_dataset_raises(self, tmp_cache):
        os = OpenSanction(cache=tmp_cache, api_key="test-key")
        with pytest.raises(ValueError, match="dataset parameter is empty"):
            await os.fetch("USA", dataset="", limit=0)
