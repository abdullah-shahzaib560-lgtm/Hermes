# Technical Analysis Data

## Snapshot Mode

Single-point-in-time dataclass with ~50 features including orderbook, trades, funding, OI, and positioning.

```python
class TechnicalSnapshot:
    symbol: str
    timestamp_ms: int
    # ... (see hermes/features/financial/models/technical.py)
```

> Snapshot mode returns a single row. Use `ta_feature.get_technical(symbol)`.

## History Mode

Time-series DataFrame with vectorized features for ML, forecasting, and anomaly detection.

```python
df = await hermes.ta_history.get_history(
    symbol="BTCUSDT",
    interval="1d",  # any canonical freq: 1s, 1m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M
    market="future",
    years=2,
)
```

### Supported Intervals

| Canonical | Binance | Description |
|-----------|---------|-------------|
| `1s` | `1s` | 1 second |
| `1m` | `1m` | 1 minute |
| `5m` | `5m` | 5 minutes |
| `15m` | `15m` | 15 minutes |
| `30m` | `30m` | 30 minutes |
| `1h` | `1h` | 1 hour |
| `2h` | `2h` | 2 hours |
| `4h` | `4h` | 4 hours |
| `6h` | `6h` | 6 hours |
| `8h` | `8h` | 8 hours |
| `12h` | `12h` | 12 hours |
| `1d` | `1d` | 1 day |
| `3d` | `3d` | 3 days |
| `1w` | `1w` | 1 week |
| `1M` | `1M` | 1 month |

### Output Columns

```python
class TechnicalHistoryRow:
    symbol: str
    timestamp_ms: int
    interval: str

    # OHLCV
    open, high, low, close, volume, quote_volume, taker_buy_volume: float

    # Returns
    ret_1b: float              # log(close_t / close_{t-1})
    ret_open_to_close: float   # close/open - 1

    # Range
    hl_range: float            # (high - low) / close
    body_range: float          # |close - open| / close

    # Moving averages
    dist_sma_20: float         # (close - SMA20) / SMA20
    dist_sma_50: float
    dist_sma_200: float
    ema_diff_9_21: float       # (EMA9 - EMA21) / EMA21
    ema_diff_21_50: float

    # Volatility
    vol_20: float              # 20-bar log return std
    vol_60: float
    atr_14_norm: float         # ATR14 / close

    # Volume
    volume_sma_20: float
    volume_rel_20: float       # volume / SMA20(volume)
    taker_buy_vol_ratio: float

    # Momentum
    rsi_14: float              # Wilder RSI
    macd: float                # EMA12 - EMA26
    macd_signal: float         # EMA9 of MACD
    macd_hist: float           # MACD - signal

    # Bollinger Bands
    bb_upper: float            # SMA20 + 2*std
    bb_lower: float            # SMA20 - 2*std
    bb_width: float            # (upper - lower) / mid
    bb_pct: float              # (close - lower) / (upper - lower)

    # Volume trend
    obv: float                 # On-Balance Volume (cumulative)

    # Distribution
    returns_skew_20: float     # Rolling skew of returns
    returns_kurt_20: float     # Rolling kurtosis of returns

    # Risk
    drawdown: float            # (close - peak) / peak
    amihud_illiquidity: float  # |ret| / quote_volume
```

> History mode uses vectorized pandas/numpy for performance. Returns a DataFrame, not a dataclass.