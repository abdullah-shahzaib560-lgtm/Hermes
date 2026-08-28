from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import aiohttp
import pytest

from hermes.connectors.binance import Binance


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


class TestBinanceBuildUrl:
    def test_spot_ohlcv(self):
        b = Binance(cache=None)
        url, params = b._build_url("spot", "ohlcv", "BTCUSDT", interval="1d", limit="30")
        assert "api.binance.com" in url
        assert params["symbol"] == "BTCUSDT"
        assert params["interval"] == "1d"
        assert params["limit"] == "30"

    def test_future_trades(self):
        b = Binance(cache=None)
        url, params = b._build_url("future", "trades", "BTCUSDT", limit="100")
        assert "fapi.binance.com" in url
        assert params["symbol"] == "BTCUSDT"

    def test_unknown_endpoint(self):
        b = Binance(cache=None)
        with pytest.raises(ValueError, match="unknown endpoint"):
            b._build_url("spot", "nonexistent", "BTCUSDT")

    def test_missing_required_param(self):
        b = Binance(cache=None)
        with pytest.raises(ValueError, match="requires"):
            b._build_url("spot", "ohlcv", "BTCUSDT")

    def test_order_book(self):
        b = Binance(cache=None)
        url, params = b._build_url("spot", "order_book", "BTCUSDT", limit="20")
        assert "depth" in url
        assert params["limit"] == "20"

    def test_funding_rate(self):
        b = Binance(cache=None)
        url, params = b._build_url("future", "fundingRate", "BTCUSDT", limit="5")
        assert "fundingRate" in url


class TestBinanceFetch:
    async def test_fetch_success(self):
        b = Binance(cache=None)
        mock_response = [[1711900800000, "65000", "65500", "64800", "65200", "1000"]]
        mock_resp = _mock_aiohttp_response(mock_response)
        mock_session = _mock_session(mock_resp)

        with patch("hermes.connectors.binance.connector.aiohttp.ClientSession", return_value=mock_session):
            result = await b._fetch(mode="spot", endpoint="ohlcv", symbol="BTCUSDT", interval="1d", limit=30)
            assert result == mock_response

    async def test_fetch_404(self):
        b = Binance(cache=None)
        mock_resp = _mock_aiohttp_response({}, status=404)
        mock_session = _mock_session(mock_resp)

        with patch("hermes.connectors.binance.connector.aiohttp.ClientSession", return_value=mock_session):
            result = await b._fetch(mode="spot", endpoint="ohlcv", symbol="BAD", interval="1d", limit=30)
            assert result is None

    async def test_fetch_403_retries(self):
        b = Binance(cache=None)
        mock_resp_403 = _mock_aiohttp_response({}, status=403)
        mock_resp_ok = _mock_aiohttp_response([[1711900800000, "65000", "65500", "64800", "65200", "1000"]])
        mock_session = AsyncMock()
        mock_session.get = AsyncMock(side_effect=[mock_resp_403, mock_resp_ok])
        mock_session.__aenter__ = AsyncMock(return_value=mock_session)
        mock_session.__aexit__ = AsyncMock(return_value=False)

        with patch("hermes.connectors.binance.connector.aiohttp.ClientSession", return_value=mock_session):
            result = await b._fetch(mode="spot", endpoint="ohlcv", symbol="BTCUSDT", interval="1d", limit=30)
            assert result is not None

    async def test_fetch_http_error(self):
        b = Binance(cache=None)
        mock_resp = _mock_aiohttp_response({}, status=500)
        mock_session = _mock_session(mock_resp)

        with patch("hermes.connectors.binance.connector.aiohttp.ClientSession", return_value=mock_session):
            with pytest.raises(aiohttp.ClientResponseError):
                await b._fetch(mode="spot", endpoint="ohlcv", symbol="BTCUSDT", interval="1d", limit=30)

    async def test_fetch_returns_data(self, tmp_cache):
        b = Binance(cache=tmp_cache)
        mock_response = [[1711900800000, "65000", "65500", "64800", "65200", "1000"]]
        mock_resp = _mock_aiohttp_response(mock_response)
        mock_session = _mock_session(mock_resp)

        with patch("hermes.connectors.binance.connector.aiohttp.ClientSession", return_value=mock_session):
            r1 = await b.fetch(mode="spot", endpoint="ohlcv", symbol="BTCUSDT", interval="1d", limit=30)
            assert r1 == mock_response
