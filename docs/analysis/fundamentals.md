# Fundamental Analysis Data

## Snapshot Mode

Single-point-in-time dataclass with SEC filings, Finnhub metrics, Yahoo Finance estimates, and FRED macro data.

```python
class CompanyFundamental:
    ticker: str
    filing_date: date
    # ... (see hermes/core/models/analysis/fundamental.py)
```

> Snapshot mode returns a single row. Use `fa_features.get_fundamentels(symbol)`.

## History Mode

### Candle History (Stock OHLCV)

```python
df = await hermes.fa_history.get_candle_history(
    symbol="AAPL",
    interval="1d",  # 1m, 5m, 15m, 30m, 1h, 1d, 1w, 1M
    years=2,
)
```

#### Supported Intervals

| Canonical | Finnhub | yfinance | Notes |
|-----------|---------|----------|-------|
| `1m` | `1` | `1m` | Finnhub: 7 days max |
| `5m` | `5` | `5m` | Finnhub: 7 days max |
| `15m` | `15` | `15m` | Finnhub: 30 days max |
| `30m` | `30` | `30m` | Finnhub: 30 days max |
| `1h` | `60` | `1h` | Finnhub: 30 days max |
| `1d` | `D` | `1d` | Finnhub: 365 days |
| `1w` | `W` | `1wk` | Finnhub: 365 days |
| `1M` | `M` | `1mo` | Finnhub: 365 days |

> Automatically falls back to yfinance if Finnhub data is insufficient (>1yr needed).

### Filing History (SEC Financials)

```python
df = await hermes.fa_history.get_filing_history(
    symbol="AAPL",
    quarters=8,  # number of historical quarters to fetch
)
```

Returns a DataFrame with one row per fiscal quarter, including all SEC XBRL fields (revenue, net income, EPS, assets, liabilities, cash flows, etc.).