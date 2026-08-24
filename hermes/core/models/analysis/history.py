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
