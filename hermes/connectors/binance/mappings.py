BINANCE_ENDPOINTS = {
    ("spot", "ohlcv"): ("api/v3/klines", ("interval", "limit")),
    ("spot", "trades"): ("api/v3/trades", ("limit",)),
    ("spot", "aggregated_trades"): ("api/v3/aggTrades", ("limit",)),
    ("spot", "order_book"): ("api/v3/depth", ("limit",)),
    ("spot", "best_bid_ask"): ("api/v3/ticker/bookTicker", ()),
    ("spot", "24hr"): ("api/v3/ticker/24hr", ()),
    ("spot", "exchangeInfo"): ("api/v3/exchangeInfo", ()),
    ("future", "ohlcv"): ("fapi/v1/klines", ("interval", "limit")),
    ("future", "trades"): ("fapi/v1/trades", ("limit",)),
    ("future", "aggregated_trades"): ("fapi/v1/aggTrades", ("limit",)),
    ("future", "order_book"): ("fapi/v1/depth", ("limit",)),
    ("future", "best_bid_ask"): ("fapi/v1/ticker/bookTicker", ()),
    ("future", "24hr"): ("fapi/v1/ticker/24hr", ()),
    ("future", "fundingRate"): ("fapi/v1/fundingRate", ("limit",)),
    ("future", "openInterest"): ("fapi/v1/openInterest", ()),
    ("future", "premiumIndex"): ("fapi/v1/premiumIndex", ()),
    ("future", "openInterestHist"): ("futures/data/openInterestHist", ("period", "limit")),
    ("future", "longShortRatio"): ("futures/data/globalLongShortAccountRatio", ("period", "limit")),
    ("future", "topLongShortAccountRatio"): ("futures/data/topLongShortAccountRatio", ("period", "limit")),
    ("future", "topLongShortPositionRatio"): ("futures/data/topLongShortPositionRatio", ("period", "limit")),
}

__all__ = ["BINANCE_ENDPOINTS"]
