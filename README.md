# Hermes

Foundational intelligence data platform for acquiring, validating, normalizing, storing, and serving country risk datasets.

Hermes is the data layer between external public data sources (World Bank, IMF, GDELT, OpenSanctions, ...) and your application. It provides a unified Python API for fetching raw indicators, computing ~60 country risk features, and building time-series or ML training panels — with built-in caching, retries, and normalization.

## Features

- **Unified connectors** — one consistent API over multiple sources:
  - [World Bank](https://data.worldbank.org/) — GDP, inflation, unemployment, governance, debt, and more (indicators API, no key needed)
  - [IMF](https://www.imf.org/) — SDMX 3.0 dataflows (IFS, WEO, GFS, ...)
  - [GDELT](https://www.gdeltproject.org/) — conflict/protest/diplomacy events via the Doc API and daily exports, with FIPS→ISO3 normalization and a canonical event schema
  - [OpenSanctions](https://www.opensanctions.org/) — sanctions datasets (`us_ofac_sdn`, `eu_fsf`, `uk_fcdos`, `un_sc`, ...), requires an API key
  - HDX CPI — bundled Corruption Perceptions Index dataset
- **60+ country risk features** across five groups:
  - `economic` — GDP growth, inflation, unemployment, debt, reserves, banking health, ...
  - `geopolitical` — conflict events, Goldstein scale, battle deaths, sanctions, governance/WGI, democracy, ...
  - `security` — military spending, alliances (NATO), arms transfers, peacekeeping
  - `social` — stability index, human rights, fragility, HDI, Gini, poverty
  - `environmental` — climate vulnerability/readiness, disaster risk, food prices, energy dependence, water stress
- **Two output modes per feature** — `"F"` returns the latest float snapshot, `"ML"` returns a monthly `pd.Series` for modeling
- **Raw cache** — Parquet-backed disk cache (`~/.hermes_cache/raw`) with per-source TTLs, hit/miss stats, and expiry-based eviction
- **Training panels** — `build_training_panel()` assembles a multi-country, monthly time-series DataFrame ready for ML
- **Export helpers** — save any result to CSV, JSON, or Parquet

## Installation

Requires Python >= 3.11. The project is managed with [uv](https://docs.astral.sh/uv/).

```bash
git clone <repo-url> Hermes
cd Hermes
uv sync --extra dev   # or: uv sync
```

## Setup

Copy the environment template and add your OpenSanctions API key:

```bash
cp .env.example .env
# add: OPEN_SANCTIONS_API=your_key_here
```

An API key is required to instantiate the main `Hermes` facade (a `KeyError` is raised otherwise).

## Quick start

```python
from hermes import Hermes
from dotenv import load_dotenv
import os

load_dotenv()

hr = Hermes(opensanction_api=os.getenv("OPEN_SANCTIONS_API"))

# Every supported country code (ISO3)
print(hr.list_countries)

# All available feature functions
print(hr.list_features)
```

### Fetch raw data from a connector

```python
# World Bank indicator time series
df = hr.world_bank.fetch(country_code="USA", indicator_code="NY.GDP.MKTP.KD.ZG")

# GDELT events by country and theme
events = hr.gdelt.query_events(countries=["UKR"], themes=["CONFLICT"])

# OpenSanctions dataset (e.g. US OFAC SDN list)
sanc = hr.opensanction.fetch(country="RUS", dataset="us_ofac_sdn")

# IMF SDMX dataflow
imf_df = hr.imf.fetch(country="USA", agency="IFS", dataflow_id="IFS", key="NGDP_R")
```

### Country risk snapshot

```python
risk = hr.features.get_country_risk_features("UKR")
print(risk["economic"]["gdp_growth_yoy"])
print(risk["geopolitical"]["conflict_event_count_30d"])
```

### Build an ML training panel

```python
panel = hr.features.build_training_panel(
    fns=[hr.lf.eco.gdp_growth_yoy, hr.lf.eco.inflation_cpi_yoy],
    countries=["USA", "UKR", "DEU"],
)
```

### Cache management

```python
hr.cache_stats()  # files, hits/misses, hit rates per source
hr.clear_cache()  # wipe everything
hr.clear_cache(older_than="7d")  # only entries older than 7 days
```

## Project layout

```
hermes/
├── __init__.py            # Hermes facade (connectors + features + cache)
├── core/
│   ├── cache.py           # RawCache: parquet-backed disk cache with TTLs
│   ├── countries.py       # supported ISO3 country codes
│   ├── export.py          # export DataFrame/Series to csv/json/parquet
│   ├── feature_decorator.py  # @feature decorator + lineage graph
│   └── features.py        # registry of all feature functions
├── features/
│   └── country_risk_features/
│       ├── pipeline.py    # risk snapshot + training panel builder
│       ├── economic.py    # geopolitical.py · security.py · social.py · environmental.py
├── sources/               # connectors: world_bank, imf, gdelt, opensanctions, hdx_cpi
tests/                     # pytest suite (respx-mocked API tests)
docs/                      # React-based documentation site
```

Every feature function is registered via the `@feature(name, group, deps, compute)` decorator, which populates a lineage graph used to resolve dependency tiers for a group.

## Development

```bash
uv run pytest                 # run tests
uv run pytest --cov=hermes    # test with coverage
uv run ruff check .           # lint
uv run ruff format .          # format
uv run mypy hermes            # type check
```

## License

MIT — see [LICENSE.md](LICENSE.md).
