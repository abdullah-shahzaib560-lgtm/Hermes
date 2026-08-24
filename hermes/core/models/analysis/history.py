from dataclasses import dataclass


@dataclass
class TechnicalHistoryRow:
    symbol: str
    timestamp_ms: int
    interval: str

    open: float
    high: float
    low: float
    close: float
    volume: float
    quote_volume: float
    taker_buy_volume: float

    ret_1b: float
    ret_open_to_close: float
    ret_3b: float
    ret_5b: float
    ret_10b: float
    ret_20b: float
    ret_60b: float

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

    volume_sma_20: float
    volume_rel_20: float
    taker_buy_vol_ratio: float

    rsi_14: float
    macd: float
    macd_signal: float
    macd_hist: float

    bb_upper: float
    bb_lower: float
    bb_width: float
    bb_pct: float

    obv: float

    returns_skew_20: float
    returns_kurt_20: float

    drawdown: float
    amihud_illiquidity: float

    return_mean_20: float
    return_std_20: float
    return_zscore_20: float
    return_zscore_60: float

    upper_wick: float
    lower_wick: float
    upper_wick_ratio: float
    lower_wick_ratio: float
    body_to_range: float

    price_zscore_20: float
    price_zscore_50: float
    price_zscore_200: float

    high_distance_20: float
    low_distance_20: float

    volume_zscore_20: float
    volume_zscore_60: float
    volume_change_1: float
    volume_change_5: float
    volume_trend_20: float
    vol_ratio_20_60: float

    vol_change_1: float
    vol_change_5: float
    atr_ratio: float

    rsi_change_1: float
    rsi_change_5: float
    macd_hist_change_1: float
    macd_hist_change_5: float
    macd_hist_zscore_20: float

    bb_width_change: float
    bb_width_zscore_20: float
    bb_pct_change: float

    buy_pressure_change: float

    trade_count_change: float
    trade_count_zscore_20: float
    avg_trade_size: float
    avg_trade_size_zscore_20: float

    drawdown_change: float
    drawdown_duration: float
    recovery_from_drawdown: float
