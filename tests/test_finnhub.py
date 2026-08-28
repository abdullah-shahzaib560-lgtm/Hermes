from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import aiohttp
import pytest

from hermes.connectors.finnhub import FINNHUB


def _mock_aiohttp_response(json_data, status=200):
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
    mock_session = AsyncMock()
    mock_session.get = AsyncMock(return_value=mock_resp)
    mock_session.__aenter__ = AsyncMock(return_value=mock_session)
    mock_session.__aexit__ = AsyncMock(return_value=False)
    return mock_session


class TestFinnhubBuildUrl:
    def test_valid_endpoints(self):
        finn = FINNHUB(api="test-key", cache=None)
        for endpoint in [
            "quote",
            "profile",
            "metric",
            "peers",
            "earnings",
            "insider",
            "eps",
            "ebitda",
            "revenue",
            "news",
            "symbol",
            "candles",
        ]:
            url = finn.build_url(endpoint)
            assert url.startswith("https://finnhub.io/api/v1/")

    def test_quote_url(self):
        finn = FINNHUB(api="test-key", cache=None)
        url = finn.build_url("quote")
        assert url.endswith("/quote")

    def test_invalid_endpoint(self):
        finn = FINNHUB(api="test-key", cache=None)
        with pytest.raises(ValueError, match="Unsupported endpoint"):
            finn.build_url("nonexistent")


class TestFinnhubFetch:
    async def test_fetch_quote(self):
        finn = FINNHUB(api="test-key", cache=None)
        mock_response = {"c": 150.0, "d": 2.5, "dp": 1.69, "h": 152.0, "l": 148.0, "o": 149.0, "pc": 147.5}
        mock_resp = _mock_aiohttp_response(mock_response)
        mock_session = _mock_session(mock_resp)

        with patch("hermes.connectors.finnhub.connector.aiohttp.ClientSession", return_value=mock_session):
            result = await finn._fetch(endpoint="quote", symbol="AAPL")
            assert result["c"] == 150.0

    async def test_fetch_profile(self):
        finn = FINNHUB(api="test-key", cache=None)
        mock_response = {"ticker": "AAPL", "name": "Apple Inc.", "exchange": "NASDAQ"}
        mock_resp = _mock_aiohttp_response(mock_response)
        mock_session = _mock_session(mock_resp)

        with patch("hermes.connectors.finnhub.connector.aiohttp.ClientSession", return_value=mock_session):
            result = await finn._fetch(endpoint="profile", symbol="AAPL")
            assert result["ticker"] == "AAPL"

    async def test_fetch_candles_requires_params(self):
        finn = FINNHUB(api="test-key", cache=None)
        with pytest.raises(ValueError, match="requires resolution"):
            await finn._fetch(endpoint="candles", symbol="AAPL")

    async def test_fetch_404(self):
        finn = FINNHUB(api="test-key", cache=None)
        mock_resp = _mock_aiohttp_response({}, status=404)
        mock_session = _mock_session(mock_resp)

        with patch("hermes.connectors.finnhub.connector.aiohttp.ClientSession", return_value=mock_session):
            result = await finn._fetch(endpoint="quote", symbol="BAD")
            assert result is None

    async def test_fetch_http_error(self):
        finn = FINNHUB(api="test-key", cache=None)
        mock_resp = _mock_aiohttp_response({}, status=500)
        mock_session = _mock_session(mock_resp)

        with patch("hermes.connectors.finnhub.connector.aiohttp.ClientSession", return_value=mock_session):
            with pytest.raises(aiohttp.ClientResponseError):
                await finn._fetch(endpoint="quote", symbol="AAPL")

    async def test_fetch_returns_data(self, tmp_cache):
        finn = FINNHUB(api="test-key", cache=tmp_cache)
        mock_response = {"c": 150.0, "d": 2.5}
        mock_resp = _mock_aiohttp_response(mock_response)
        mock_session = _mock_session(mock_resp)

        with patch("hermes.connectors.finnhub.connector.aiohttp.ClientSession", return_value=mock_session):
            r1 = await finn.fetch(endpoint="quote", symbol="AAPL")
            assert r1 == mock_response
