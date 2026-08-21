# hermes/core/models/analysis/technical.py
from dataclasses import dataclass
from typing import Optional
from datetime import datetime
from hermes.core.models.analysis.fundamental import CompanyFundamental

@dataclass
class TechnicalSnapshot:
    """
    Latest technical state for a ticker.
    """
    symbol: str

    # Latest bar
    timestamp: Optional[datetime] = None
    open: Optional[float] = None
    high: Optional[float] = None
    low: Optional[float] = None
    close: Optional[float] = None
    volume: Optional[int] = None

    # Trend
    sma_20: Optional[float] = None
    sma_50: Optional[float] = None
    sma_200: Optional[float] = None
    ema_12: Optional[float] = None
    ema_26: Optional[float] = None

    # Momentum
    rsi_14: Optional[float] = None
    macd_line: Optional[float] = None
    macd_signal: Optional[float] = None
    macd_hist: Optional[float] = None
    stochastic_k: Optional[float] = None
    stochastic_d: Optional[float] = None
    momentum_1m: Optional[float] = None
    momentum_3m: Optional[float] = None
    momentum_6m: Optional[float] = None

    # Volatility
    atr_14: Optional[float] = None
    historical_vol_20d: Optional[float] = None

    # Volume
    obv: Optional[float] = None
    vwap: Optional[float] = None
    avg_volume_20d: Optional[float] = None
    volume_ratio: Optional[float] = None  # today vs avg

    # Bands & trend strength
    bb_upper: Optional[float] = None
    bb_middle: Optional[float] = None
    bb_lower: Optional[float] = None
    adx_14: Optional[float] = None

    # Pattern / level flags (you can expand)
    above_sma_50: Optional[bool] = None
    above_sma_200: Optional[bool] = None
    breakout_20d_high: Optional[bool] = None
    trend_direction: Optional[str] = None  # "Bullish", "Bearish", "Neutral"
    momentum_state: Optional[str] = None   # "Strong", "Moderate", "Weak"
    volatility_state: Optional[str] = None # "High", "Moderate", "Low"
    volume_state: Optional[str] = None     # "Positive", "Neutral", "Negative"

