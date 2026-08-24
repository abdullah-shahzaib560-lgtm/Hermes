from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import numpy as np
import pandas as pd
import pytest

from hermes.constants import (
    BINANCE_INTERVAL_MAP,
    BINANCE_INTERVAL_MS,
    CANONICAL_FREQS,
    FINNHUB_MAX_DAYS,
    FINNHUB_RESOLUTION_MAP,
    YFINANCE_INTERVAL_MAP,
)
from hermes.features.analysis.history import TAHistory, _macd, _obv, _rsi


class TestFreqMappings:
    def test_all_canonical_freqs_mapped_to_binance(self):
        for freq in CANONICAL_FREQS:
            assert freq in BINANCE_INTERVAL_MAP, f"{freq} missing from BINANCE_INTERVAL_MAP"
            assert BINANCE_INTERVAL_MAP[freq] is not None

    def test_binance_interval_ms_covers_all(self):
        for freq in CANONICAL_FREQS:
            assert freq in BINANCE_INTERVAL_MS, f"{freq} missing from BINANCE_INTERVAL_MS"
            assert BINANCE_INTERVAL_MS[freq] > 0

    def test_finnhub_resolution_map_covers_stock_freqs(self):
        stock_freqs = ["1m", "5m", "15m", "30m", "1h", "1d", "1w", "1M"]
        for freq in stock_freqs:
            assert freq in FINNHUB_RESOLUTION_MAP, f"{freq} missing from FINNHUB_RESOLUTION_MAP"

    def test_yfinance_interval_map_covers_stock_freqs(self):
        stock_freqs = ["1m", "5m", "15m", "30m", "1h", "1d", "1w", "1M"]
        for freq in stock_freqs:
            assert freq in YFINANCE_INTERVAL_MAP, f"{freq} missing from YFINANCE_INTERVAL_MAP"

    def test_finnhub_max_days_has_all_resolutions(self):
        for res in FINNHUB_RESOLUTION_MAP.values():
            assert res in FINNHUB_MAX_DAYS, f"Resolution {res!r} missing from FINNHUB_MAX_DAYS"

    def test_binance_ms_values_correct(self):
        assert BINANCE_INTERVAL_MS["1m"] == 60_000
        assert BINANCE_INTERVAL_MS["1h"] == 3_600_000
        assert BINANCE_INTERVAL_MS["1d"] == 86_400_000
        assert BINANCE_INTERVAL_MS["1w"] == 604_800_000


def _make_ohlcv_df(n: int = 250, start_price: float = 100.0) -> pd.DataFrame:
    np.random.seed(42)
    prices = start_price + np.cumsum(np.random.randn(n) * 0.5)
    prices = np.maximum(prices, 1.0)
    return pd.DataFrame(
        {
            "open_time": np.arange(n) * 86_400_000,
            "open": prices * 0.99,
            "high": prices * 1.02,
            "low": prices * 0.98,
            "close": prices,
            "volume": np.random.uniform(1000, 5000, n),
            "quote_volume": np.random.uniform(100000, 500000, n),
            "taker_buy_volume": np.random.uniform(500, 2500, n),
        }
    )


class TestTAHistoryFeatures:
    def test_compute_features_output_columns(self):
        df = _make_ohlcv_df(250)
        df["symbol"] = "BTCUSDT"
        df["interval"] = "1d"
        result = TAHistory._compute_features(df)

        expected_cols = [
            "ret_1b",
            "ret_open_to_close",
            "hl_range",
            "body_range",
            "dist_sma_20",
            "dist_sma_50",
            "dist_sma_200",
            "ema_diff_9_21",
            "ema_diff_21_50",
            "vol_20",
            "vol_60",
            "atr_14_norm",
            "volume_sma_20",
            "volume_rel_20",
            "taker_buy_vol_ratio",
            "rsi_14",
            "macd",
            "macd_signal",
            "macd_hist",
            "bb_upper",
            "bb_lower",
            "bb_width",
            "bb_pct",
            "obv",
            "returns_skew_20",
            "returns_kurt_20",
            "drawdown",
            "amihud_illiquidity",
        ]
        for col in expected_cols:
            assert col in result.columns, f"Missing column: {col}"

    def test_compute_features_preserves_original_cols(self):
        df = _make_ohlcv_df(250)
        df["symbol"] = "BTCUSDT"
        df["interval"] = "1d"
        result = TAHistory._compute_features(df)

        assert "open" in result.columns
        assert "close" in result.columns
        assert "volume" in result.columns
        assert "symbol" in result.columns
        assert "interval" in result.columns

    def test_compute_features_row_count(self):
        df = _make_ohlcv_df(250)
        df["symbol"] = "BTCUSDT"
        df["interval"] = "1d"
        result = TAHistory._compute_features(df)
        assert len(result) == 250

    def test_rsi_bounded(self):
        closes = 100.0 + np.cumsum(np.random.randn(100) * 0.5)
        rsi = _rsi(closes, 14)
        valid = rsi[~np.isnan(rsi)]
        assert len(valid) > 0
        assert valid.min() >= 0
        assert valid.max() <= 100

    def test_macd_returns_three_arrays(self):
        closes = 100.0 + np.cumsum(np.random.randn(100) * 0.5)
        macd, signal, hist = _macd(closes)
        assert len(macd) == len(closes)
        assert len(signal) == len(closes)
        assert len(hist) == len(closes)

    def test_obv_monotonic_increasing_uptrend(self):
        closes = np.arange(1.0, 51.0)
        volumes = np.ones(50) * 100
        obv = _obv(closes, volumes)
        assert np.all(np.diff(obv) >= 0)

    def test_drawdown_always_non_positive(self):
        df = _make_ohlcv_df(250)
        df["symbol"] = "BTCUSDT"
        df["interval"] = "1d"
        result = TAHistory._compute_features(df)
        valid = result["drawdown"].dropna()
        assert (valid <= 0).all()

    def test_volume_rel_20_near_one_for_random(self):
        df = _make_ohlcv_df(250)
        df["symbol"] = "BTCUSDT"
        df["interval"] = "1d"
        result = TAHistory._compute_features(df)
        valid = result["volume_rel_20"].dropna()
        assert valid.mean() == pytest.approx(1.0, abs=0.1)


class TestTAHistoryAsync:
    async def test_get_history_empty(self):
        ta = TAHistory()
        with patch.object(ta.binance, "fetch_history", new_callable=AsyncMock) as mock_fetch:
            mock_fetch.return_value = pd.DataFrame()
            result = await ta.get_history("BTCUSDT", interval="1d", years=1)
            assert result.empty

    async def test_get_history_calls_features(self):
        ta = TAHistory()
        mock_df = _make_ohlcv_df(250)
        with patch.object(ta.binance, "fetch_history", new_callable=AsyncMock) as mock_fetch:
            mock_fetch.return_value = mock_df
            result = await ta.get_history("BTCUSDT", interval="1d", years=1)
            assert not result.empty
            assert "rsi_14" in result.columns
            assert "macd" in result.columns
            mock_fetch.assert_called_once()


class TestBinanceBuildUrlWithTime:
    def test_ohlcv_with_start_end_time(self):
        from hermes.sources.binance import Binance

        b = Binance(cache=None)
        url, params = b._build_url(
            "spot",
            "ohlcv",
            "BTCUSDT",
            interval="1d",
            limit="1000",
            start_time=1700000000000,
            end_time=1700100000000,
        )
        assert params["startTime"] == 1700000000000
        assert params["endTime"] == 1700100000000
        assert params["symbol"] == "BTCUSDT"

    def test_ohlcv_without_time_params(self):
        from hermes.sources.binance import Binance

        b = Binance(cache=None)
        url, params = b._build_url(
            "spot",
            "ohlcv",
            "BTCUSDT",
            interval="1d",
            limit="100",
        )
        assert "startTime" not in params
        assert "endTime" not in params
