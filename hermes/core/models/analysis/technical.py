from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Tuple


@dataclass
class TechnicalSnapshot:

    ticker: str 
    timestamp: datetime

    current_price: float
    finnhub_ohlcv: Tuple[float, float, float, float, float]

    historical_ohlcv: Dict[str, List[Tuple[float, float, float, float, float]]] = (
        field(default_factory=dict)
    )

    binance_ohlcv: Tuple[float, float, float, float, float]
    high_24h: float
    low_24h: float
    volume_24h: float

    best_bid: float
    best_ask: float
    bid_quantity: float
    ask_quantity: float

    # Order book representation: Lists of (Price, Quantity) tuples for bids and asks
    # e.g., {'bids': [(100.0, 1.5), (99.9, 2.0)], 'asks': [(100.1, 0.5)]}
    order_book: Dict[str, List[Tuple[float, float]]] = field(
        default_factory=dict
    )

    # Individual execution feed: (Trade Price, Trade Volume, Trade Timestamp)
    trades: List[Tuple[float, float, datetime]] = field(default_factory=list)

    # Aggregated trades compress multiple trades at identical prices/times:
    # (Price, Volume, First Trade ID, Last Trade ID, Timestamp)
    aggregated_trades: List[Tuple[float, float, int, int, datetime]] = field(
        default_factory=list
    )

    funding_rate: float = 0.0
    open_interest: float = 0.0
