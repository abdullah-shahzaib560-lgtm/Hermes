# Hermes

Foundational intelligence data platform for acquiring, validating, normalizing, storing, and serving country risk and financial intelligence datasets.

## What is Hermes?

Hermes is a Python data platform that sits between external public data sources (World Bank, IMF, GDELT, OpenSanctions, FRED, Binance, Finnhub, SEC EDGAR, Yahoo Finance, ...) and your application. It provides a single, unified async API for:

- **Acquiring** raw indicators, events, and financial data from heterogeneous public APIs
- **Normalizing** them into a consistent, country-keyed or ticker-keyed data model
- **Computing** ~58 country risk features across five dimensions plus technical and fundamental analysis features
- **Storing** raw responses in a TTL-based disk cache
- **Serving** both latest-value snapshots (`"F"` mode) and monthly time series (`"ML"` mode) ready for dashboards or ML training

## Why does it exist?

Country risk analysis requires stitching together dozens of unrelated public datasets: macroeconomic indicators from the World Bank and IMF, conflict and protest events from GDELT, sanctions lists from OpenSanctions, governance scores, fragile state indices, climate risk scores, and more. Each source has its own API, schema, country-code convention (ISO3 vs ISO2 vs FIPS), update cadence, and failure modes.

Additionally, financial analysis requires data from market data providers (Binance, Yahoo Finance), fundamental data providers (Finnhub, SEC EDGAR), and economic data (FRED).

Hermes exists to hide that complexity behind one facade, so analysts and engineers work with a single `Hermes` object instead of N SDKs.

## What problem does it solve?

- **Fragmentation** — one API over nine source families instead of bespoke integration code per source
- **Code mismatch** — GDELT reports FIPS codes, OpenSanctions wants ISO2, features key on ISO3; Hermes normalizes all of it
- **Repetitive network work** — every fetch is cached (Parquet-backed, per-source TTLs) and retried with backoff
- **Feature engineering duplication** — 58 battle-tested features (GDP growth, inflation volatility, conflict trends, Goldstein-scale averages, sanctions coverage, WGI governance, climate vulnerability, ...) computed consistently across countries and time
- **Two incompatible consumption modes** — the same feature returns either a latest float for a risk dashboard or a monthly `pd.Series` for a training set, with no extra code
- **Financial data fragmentation** — technical indicators, fundamentals, and macroeconomic data from different providers unified under one interface

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  Hermes facade  (hermes/__init__.py)                        │
│  connectors · feature groups · cache · listings            │
└─────────────────────────────────────────────────────────────┘
        │                        │
        ▼                        ▼
┌────────────────┐      ┌───────────────────────────────┐
│ sources/       │      │ features/                     │
│ connectors     │      │ country_risk_features         │
│                │      │ pipeline + 5 feature groups   │
│ world_bank     │◄────►│ (eco · geo · sec · soc · env) │
│ imf            │      │ @feature decorator → lineage  │
│ gdelt          │      └───────────────────────────────┘
│ opensanctions  │      │ features/analysis             │
│ public_data    │      │ technical · fundamental       │
│ fred           │      └───────────────────────────────┘
│ binance        │
│ finnhub        │
│ sec_edgar      │
│ yfinance       │
└───────┬────────┘
        ▼
┌────────────────┐
│ core/          │
│ cache (RawCache│ parquet + meta.json, TTLs, stats
│ countries      │ ISO3 listing + validation
│ export         │ csv / json / parquet
│ feature_decorator │ lineage graph, tiered plans
│ helper         │ iso3↔iso2, empty-result guards
│ models         │ pydantic models for analysis features
└────────────────┘
```

- **Facade** — `Hermes` bundles connectors, the feature pipeline, analysis features, and cache controls into one object.
- **Connectors** — one class per source family (`sources/`), each exposing an async `fetch(...)` backed by `RawCache`.
- **Feature layer** — five group modules (`economic`, `geopolitical`, `security`, `social`, `environmental`). Every feature is registered via the `@feature(name, group, deps, compute)` decorator, which populates a lineage graph (`core/feature_decorator.py`) used to resolve dependency tiers for a group.
- **Analysis features** — `TAfeatures` (technical analysis from Binance data) and `FAfeatures` (fundamental analysis from Finnhub, SEC EDGAR, FRED, Yahoo Finance).
- **Pipeline** — `get_country_risk_features()` computes all features of a group concurrently via `asyncio.gather`; `build_training_panel()` assembles multi-country monthly panels.
- **Cache** — `RawCache` stores normalized raw responses as Parquet files with sidecar `.meta.json` (params, cached_at, row/column stats), per-source TTLs, expiry-based eviction, and hit/miss statistics.

## Installation

Requires Python >= 3.11. The project is managed with [uv](https://docs.astral.sh/uv/).

```bash
git clone <repo-url> Hermes
cd Hermes
uv sync --dev        # include dev group for testing; plain `uv sync` otherwise
```

## Quickstart

Create a `.env` file with your API keys:

```bash
cp .env.example .env
# add:
# OPEN_SANCTIONS_API=your_opensanctions_key_here
# NEWS_DATA_API=your_newsdata_key_here
# FRED_API=your_fred_key_here
# FINNHUB_API=your_finnhub_key_here
# SEC_USERNAME=your_sec_edgar_username
# SEC_EMAIL=your_sec_edgar_email
```

```python
import asyncio
import os

from dotenv import load_dotenv
from hermes import Hermes

load_dotenv()

hr = Hermes(
    opensanction_api=os.getenv("OPEN_SANCTIONS_API"),
    new_data_api=os.getenv("NEWS_DATA_API"),
    fred_api=os.getenv("FRED_API"),
    sec_username=os.getenv("SEC_USERNAME"),
    sec_email=os.getenv("SEC_EMAIL"),
    finnhub_api=os.getenv("FINNHUB_API"),
)


async def main():
    # Every supported country code (ISO3) and every available feature
    print(hr.list_countries)
    print([f.__name__ for f in hr.list_features])

    # Latest country risk snapshot (all groups, computed concurrently)
    risk = await hr.country_features.get_country_risk_features("UKR")
    print(risk["economic"]["gdp_growth_yoy"])
    print(risk["geopolitical"]["conflict_event_count_30d"])

    # ML training panel: monthly series for a set of countries
    panel = await hr.country_features.build_training_panel(
        fns=[hr.lf.eco.gdp_growth_yoy, hr.lf.eco.inflation_cpi_yoy],
        countries=["USA", "UKR", "DEU"],
    )
    print(panel)

    # Cache controls
    print(hr.cache_stats())
    hr.clear_cache(older_than="7d")


asyncio.run(main())
```

## Example

Fetch raw data from any connector:

```python
# World Bank indicator time series
df = await hr.world_bank.fetch(country_code="USA", indicator_code="NY.GDP.MKTP.KD.ZG")

# GDELT events by country and theme (normalized to canonical schema)
events = await hr.gdelt.query_events(countries=["UKR"], themes=["CONFLICT"])

# OpenSanctions dataset (e.g. US OFAC SDN list) — raw JSON
sanc = await hr.opensanction.fetch(country="RUS", dataset="us_ofac_sdn")

# IMF SDMX 3.0 dataflow
imf_df = await hr.imf.fetch(country="USA", agency="IFS", dataflow_id="IFS", key="NGDP_R")

# FRED economic data
fred_df = await hr.fred.fetch(series_id="GDPC1")

# Binance market data (spot OHLCV)
ohlcv = await hr.binance.fetch(symbol="BTCUSDT", market_type="spot", endpoint="ohlcv", interval="1d", limit=30)

# Finnhub stock data
quote = await hr.finnhub.fetch(symbol="AAPL", endpoint="quote")

# SEC EDGAR company facts
facts = await hr.sec_edger.fetch(symbol="AAPL")

# Yahoo Finance earnings data
earnings = await hr.yfin.fetch(symbol="AAPL", endpoint="earnings_history")
```

Work with individual features in either mode:

```python
# "F" — latest value as a float/string/bool
gdp = await hr.lf.eco.gdp_growth_yoy(country_code="USA", mode="F")

# "ML" — monthly pd.Series (resampled, interpolated) for modeling
gdp_series = await hr.lf.eco.gdp_growth_yoy(country_code="USA", mode="ML")

# Technical analysis features
ta_snapshot = await hr.ta_feature.snapshot("BTCUSDT")

# Fundamental analysis features
fa_snapshot = await hr.fa_feature.snapshot("AAPL")

# Export anything to csv / json / parquet
from hermes.core.export import export

export(data=panel, filetype="parquet", name="training_panel")
```

## API

### Facade `Hermes`

| Member | Type | Description |
|---|---|---|
| `Hermes(opensanction_api, new_data_api, fred_api, sec_username, sec_email, finnhub_api, cache_dir=None, use_cache=True)` | ctor | API keys for various services |
| `.world_bank` / `.imf` / `.gdelt` / `.opensanction` / `.fred` / `.binance` / `.finnhub` / `.sec_edger` / `.yfin` / `.datasets` | connectors | Async data fetchers |
| `.country_features` | `pipeline` | `get_country_risk_features(country)` and `build_training_panel(fns, countries)` |
| `.ta_feature` | `TAfeatures` | Technical analysis features from Binance market data |
| `.fa_features` | `FAfeatures` | Fundamental analysis features from Finnhub, SEC EDGAR, FRED, Yahoo Finance |
| `.lf` | `features` | Feature registry: `.eco`, `.geo`, `.sec`, `.soc`, `.env` groups |
| `.list_countries` | `list[str]` | All supported ISO3 codes |
| `.list_features` | `list[Callable]` | All feature functions |
| `.clear_cache(older_than="7d")` | method | Evict cache entries (`h`/`d`/`w` units) |
| `.cache_stats()` | `dict` | Files, per-source hit/miss counts and hit rates |

### Connectors

All connectors expose `async fetch(...)` (plus `query_events(...)` for GDELT) and share `force` and retry/timeout parameters. Uses `aiohttp` for async HTTP.

### Features

Every feature is `async fn(country_code: str, mode: "F" | "ML")`:

- `"F"` — latest value: `float`, `int`, `str`, or `bool` (e.g. `nato_member`)
- `"ML"` — monthly `pd.Series` with a `DatetimeIndex`, interpolated to month-start frequency
- Missing data returns `np.nan` (`"F"`) or an empty `pd.Series` (`"ML"`) instead of raising

### Pipeline

| Method | Returns |
|---|---|
| `await pipeline.get_country_risk_features(country)` | dict: `country`, five group dicts, `metadata` (`last_updated`, `features_version`) |
| `await pipeline.build_training_panel(fns, countries)` | `pd.DataFrame` with `MultiIndex (country_iso3, date)`, one column per feature |

## Data model

- **Connector frames** — normalized `pd.DataFrame`s:
  - World Bank: `date, indicator_id, indicator_name, country, value, source`
  - IMF: `date, indicator_id, country, value, source` (+ any SDMX dimension attributes)
  - GDELT: canonical event schema `event_id, date, country_iso3, event_type, severity, lat, lon, source` (FIPS → ISO3 mapped, CAMEO/GKG themes classified into `conflict`, `protest`, `diplomacy`, `sanction`, ...)
  - OpenSanctions: raw JSON response as returned by the API
  - FRED: `date, indicator_id, indicator_name, country, value, source`
  - Binance: `date, open, high, low, close, volume, ...` (OHLCV and other market data)
  - Finnhub: varies by endpoint (quote, candles, fundamentals)
  - SEC EDGAR: company facts as structured financial data
  - Yahoo Finance: earnings estimates, revenue estimates, earnings history
- **Risk snapshot** — nested dict: `{country, economic, geopolitical, security, social, environmental, metadata}`
- **Training panel** — monthly time-series `pd.DataFrame` with `MultiIndex (country_iso3, date)`
- **Cache** — Parquet data files + sidecar `.meta.json` under `~/.hermes_cache/raw/<source>/<hash>.parquet`

## Supported sources

| Source | What it provides | Auth | Cache TTL |
|---|---|---|---|
| [World Bank](https://data.worldbank.org/) indicators API | GDP, inflation, unemployment, governance, debt, ... | none | 7 days |
| [IMF](https://www.imf.org/) SDMX 3.0 dataflows | IFS, WEO, GFS, ... | none | 7 days |
| [GDELT](https://www.gdeltproject.org/) Doc API + daily exports | conflict/protest/diplomacy events, Goldstein scale, battle deaths | none | 6 hours |
| [OpenSanctions](https://www.opensanctions.org/) | sanctions lists (`us_ofac_sdn`, `eu_fsf`, `uk_fcdos`, `un_sc`, ...) | API key | 30 days |
| [FRED](https://fred.stlouisfed.org/) | US economic indicators (GDP, CPI, unemployment, interest rates, ...) | API key | 7 days |
| [Binance](https://www.binance.com/) | cryptocurrency market data (OHLCV, trades, order book, ...) | none | varies |
| [Finnhub](https://finnhub.io/) | stock market data (quotes, candles, fundamentals, insider trades, ...) | API key | varies |
| [SEC EDGAR](https://www.sec.gov/edgar) | company financial facts (XBRL filings) | User-Agent required | 7 days |
| [Yahoo Finance](https://finance.yahoo.com/) | earnings estimates, revenue estimates, earnings history | none | 7 days |
| Bundled datasets (`sources/lib/datasets/`) | HDX CPI, Human Development Index, Fragile State Index, Human Rights Score, NATO membership, climate vulnerability/readiness, crisis risk | none | static |

### Feature groups (~58 features)

- **economic** (18) — GDP growth YoY/QoQ, CPI/PPI inflation, inflation volatility, unemployment, current account, FX reserves, external debt, fiscal deficit, government debt, REER misalignment, banking sector health, GDP per capita PPP
- **geopolitical** (21) — conflict/protest/diplomatic event counts, conflict trend, Goldstein scale, battle deaths, sanctions (count, new, sector coverage), WGI governance, CPI, rule of law, regulatory quality, democracy index, regime type, press freedom
- **security** (7) — military spending (level, growth), alliance strength, arms imports/exports, peacekeeping troops, NATO membership
- **social** (6) — social stability, human rights, fragile state index, HDI, Gini, poverty headcount
- **environmental** (6) — climate vulnerability/readiness, natural disaster risk, food price index, energy dependence, water stress

### Analysis features

- **technical** — technical indicators computed from Binance market data (SMA, EMA, RSI, MACD, Bollinger Bands, ATR, volatility metrics, mean reversion score, trend strength, momentum)
- **fundamental** — company fundamentals from Finnhub, SEC EDGAR, FRED, and Yahoo Finance (revenue, earnings, margins, ratios, valuation metrics)

## Tests

The suite is pytest-based with `unittest.mock`-patched HTTP calls (no live network) and async tests:

```bash
uv run pytest                 # run all tests
uv run pytest --cov=hermes    # run with coverage
```

Coverage is collected from the `hermes` package (`tests/` omitted); `asyncio_mode = "auto"` means async tests need no explicit markers.

### Test files

| File | Covers |
|---|---|
| `test_cache.py` | `RawCache` put/get, TTL expiry, corruption, stats, clear |
| `test_feature_decorator.py` | `@feature` decorator, `LineageGraph`, `TieredPlan` |
| `test_economic_features.py` | All 18 economic features + `core.helper` utilities |
| `test_gdelt.py` | GDELT connector, theme classification, FIPS mapping, canonical schema |
| `test_imf.py` | IMF SDMX connector, ISO3→ISO2 mapping |
| `test_opensanctions.py` | OpenSanctions connector |
| `test_world_bank.py` | World Bank connector, cache integration |
| `test_fred.py` | FRED connector, cache integration |
| `test_binance.py` | Binance connector, URL building, cache integration |
| `test_finnhub.py` | Finnhub connector, endpoint validation, cache integration |
| `test_sec_edgar.py` | SEC EDGAR connector, User-Agent header, cache integration |
| `test_yfinance.py` | Yahoo Finance connector, endpoint validation, cache integration |
| `test_pipeline.py` | Country risk pipeline, `get_country_risk_features`, `build_training_panel` |
| `test_technical_features.py` | `TAfeatures` static helpers, price features, snapshot with mocked Binance |
| `test_fundamental_features.py` | `FAfeatures` SEC extraction, filing metadata |
| `test_scheduler.py` | Cron parsing, job scheduling, execution, retries, lifecycle |
| `test_hermes.py` | `Hermes` facade initialization, cache stats, listings |

## CI

GitHub Actions (`.github/workflows/publish.yml`) runs on push/PR to `main` and on releases:

- **quality** job — matrix over Python 3.11 / 3.12 / 3.13: `ruff check .` (lint) → `mypy hermes` (type check) → `pytest --cov` (tests with coverage)
- **publish** job — on release: `uv build` and `uv publish` to PyPI (trusted publishing via `PYPI_TOKEN`)

## License

MIT — see [LICENSE.md](LICENSE.md).

## Roadmap

- **NewsData connector** — the `new_data_api` parameter is already wired into the facade; implement the news/event source it unlocks
- **Validation layer** — schema checks and outlier detection on fetched frames before caching
- **Serving layer** — REST/query interface over the feature registry so non-Python consumers can use Hermes
- **Documentation site** — dedicated docs replacing the README for API reference and source coverage
- **More sources** — SIPRI arms transfers, FAO food/water data, UN peacekeeping feeds to replace bundled static datasets
- **Broader country coverage** — fill gaps where sources lack data for smaller economies; per-feature availability reporting
