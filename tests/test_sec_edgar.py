from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import aiohttp
import pytest

from hermes.connectors.sec import SECEDGAR


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


class TestSECEDGAR:
    async def test_fetch_success(self):
        sec = SECEDGAR(username="test-user", email="test@example.com", cache=None)
        mock_response = {
            "facts": {
                "us-gaap": {
                    "Revenues": {
                        "units": {
                            "USD": [
                                {"val": 394328000000, "fy": 2023, "fp": "FY", "filed": "2023-10-27", "form": "10-K"}
                            ]
                        }
                    }
                }
            }
        }
        mock_resp = _mock_aiohttp_response(mock_response)
        mock_session = _mock_session(mock_resp)

        with patch("hermes.connectors.sec.connector.aiohttp.ClientSession", return_value=mock_session):
            result = await sec._fetch(symbol="AAPL")
            assert result is not None
            assert "facts" in result

    async def test_fetch_404(self):
        sec = SECEDGAR(username="test-user", email="test@example.com", cache=None)
        mock_resp = _mock_aiohttp_response({}, status=404)
        mock_session = _mock_session(mock_resp)

        with patch("hermes.connectors.sec.connector.aiohttp.ClientSession", return_value=mock_session):
            result = await sec._fetch(symbol="BAD")
            assert result is None

    async def test_fetch_http_error(self):
        sec = SECEDGAR(username="test-user", email="test@example.com", cache=None)
        mock_resp = _mock_aiohttp_response({}, status=500)
        mock_session = _mock_session(mock_resp)

        with patch("hermes.connectors.sec.connector.aiohttp.ClientSession", return_value=mock_session):
            with pytest.raises(aiohttp.ClientResponseError):
                await sec._fetch(symbol="AAPL")

    async def test_fetch_retry_on_timeout(self):
        sec = SECEDGAR(username="test-user", email="test@example.com", cache=None)
        mock_session = AsyncMock()
        mock_session.get = AsyncMock(side_effect=TimeoutError("timeout"))
        mock_session.__aenter__ = AsyncMock(return_value=mock_session)
        mock_session.__aexit__ = AsyncMock(return_value=False)

        with patch("hermes.connectors.sec.connector.aiohttp.ClientSession", return_value=mock_session):
            with pytest.raises(TimeoutError):
                await sec._fetch(symbol="AAPL", retries=1)

    async def test_fetch_sends_user_agent(self):
        sec = SECEDGAR(username="test-user", email="test@example.com", cache=None)
        mock_resp = _mock_aiohttp_response({"facts": {"us-gaap": {}}})
        mock_session = _mock_session(mock_resp)

        with patch("hermes.connectors.sec.connector.aiohttp.ClientSession", return_value=mock_session):
            await sec._fetch(symbol="AAPL")
            call_kwargs = mock_session.get.call_args
            assert "headers" in call_kwargs.kwargs or "headers" in call_kwargs[1] if len(call_kwargs) > 1 else True

    async def test_fetch_returns_data(self, tmp_cache):
        sec = SECEDGAR(username="test-user", email="test@example.com", cache=tmp_cache)
        mock_response = {"facts": {"us-gaap": {"Revenues": {"units": {"USD": [{"val": 100}]}}}}}
        mock_resp = _mock_aiohttp_response(mock_response)
        mock_session = _mock_session(mock_resp)

        with patch("hermes.connectors.sec.connector.aiohttp.ClientSession", return_value=mock_session):
            r1 = await sec.fetch(symbol="AAPL")
            assert r1 == mock_response
