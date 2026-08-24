# Technical Analysis Data

## Current Data Format

```python
class TechnicalSnapshot:
    symbol: str
    timestamp_ms: int

    open: float
    high: float
    low: float
    close: float
    volume: float
    quote_volume: float
    trades_count: int

    ret_1b: float
    ret_5b: float
    ret_10b: float
    ret_60b: float
    ret_open_to_close: float

    hl_range: float
    body_range: float

    dist_sma_20: float
    dist_sma_50: float
    dist_sma_200: float

    ema_diff_9_21: float
    ema_diff_21_50: float

    vol_20: float
    vol_60: float
    atr_14_norm: float

    volume_rel_20: float
    taker_buy_vol_ratio: float

    trade_window_count: int
    trade_window_vol_base: float
    trade_window_vol_quote: float
    trade_buy_vol_ratio: float
    avg_trade_size: float
    median_trade_size: float
    large_trade_vol_ratio: float

    bid_price: float
    ask_price: float
    bid_qty: float
    ask_qty: float

    spread_abs: float
    spread_bps: float
    top_book_imbalance: float

    depth_bid_total: float
    depth_ask_total: float
    depth_imbalance: float

    high_24h: float
    low_24h: float
    last_price_24h: float
    range_24h: float
    pct_change_24h: float
    pos_in_24h_range: float
    volume_24h: float
    quote_volume_24h: float

    funding_rate: float
    funding_rate_lag_3: float
    funding_rate_change: float
    funding_rate_zscore: float

    time_to_next_funding_min: float

    open_interest: float
    oi_change_1h: float
    oi_change_24h: float
    oi_to_volume_24h: float

    trend_score: float
    mean_reversion_score: float
    liquidity_score: float
    order_flow_score: float
    sentiment_score: float

```

> For now it is basically a snapshot, means a single row or a point in time. In the future, we will add a time series of technical indicators, so that we can analyze trends over time.