from sec_cik_mapper import StockMapper


def get_cik(ticker: str) -> str:
    mapper = StockMapper()
    ticker_to_cik_dict = mapper.ticker_to_cik  # type: ignore[operator]

    cik = ticker_to_cik_dict.get(ticker.upper())
    return f"CIK{cik}" if cik else "Not Found"


__all__ = ["get_cik"]
