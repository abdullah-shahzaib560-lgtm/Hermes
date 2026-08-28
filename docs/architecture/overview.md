# Hermes Architecture Overview

This document describes the target (current) package layout of the `hermes` package and the
responsibilities of each subsystem.

> Written during the Repository Refactor (checklist Section 1). For a section-by-section
> description of every planned module, see [`codebase.md`](codebase.md).

## Top-level layout

```
hermes/
├── __init__.py          # Hermes facade: bundles connectors, features, cache, listings
├── acquisition/         # acquisition infrastructure
│   ├── cache.py         # RawCache: Parquet + meta.json, per-source TTLs, stats
│   └── client.py        # async HTTP client scaffolding (in progress)
├── connectors/          # one package per external source family
│   ├── binance/         #   connector.py · parser.py · normalizer.py · mappings.py
│   ├── finnhub/
│   ├── fred/
│   ├── gdelt/           # stub (helpers.py · mappings.py preserved for rebuild)
│   ├── imf/
│   ├── opensanctions/
│   ├── public_data/     # bundled static datasets under connectors/lib/datasets/
│   ├── sec/             #   + tags.py (SEC_TAG_MAP)
│   ├── world_bank/
│   ├── yfinance/
│   └── lib/             # shared bundled datasets (CSVs)
├── core/                # minimal cross-cutting infrastructure
│   └── scheduler.py     # generic cron scheduler
├── entities/            # domain entities and lookup helpers
│   ├── countries.py     # ISO3 listing, iso3↔iso2, check_iso3
│   └── companies.py     # ticker → CIK (SEC)
├── export/              # csv / json / parquet export helpers
├── features/            # feature engineering
│   ├── decorator.py     # @feature, LineageGraph, TieredPlan
│   ├── registry.py      # `features` facade: eco/env/geo/sec/soc groups + list_features
│   ├── country_risk_features/
│   │   ├── economic.py · environmental.py · geopolitical.py (stub) ·
│   │   │   security.py · social.py
│   │   ├── pipeline.py  # get_country_risk_features, build_training_panel
│   │   └── utils.py     # check_empty, empty_result, adjust_year_range
│   └── financial/
│       ├── technical.py     # TAfeatures
│       ├── fundamental.py   # FAfeatures
│       ├── crpto.py         # CryptoHistory + K-line helpers
│       ├── filling.py       # CompanyFiling + filing helpers
│       └── models/          # dataclass/column models
│           ├── technical.py · fundamental.py · history.py
└── constants.py         # shared frequency/resolution maps
```

## Responsibilities by subsystem

| Subsystem | Owns | Not owned here |
|---|---|---|
| `hermes/__init__.py` | Public `Hermes` facade, cache controls, listings | feature logic |
| `acquisition/` | Raw caching, HTTP client mechanics, retries | per-source fetch logic |
| `connectors/` | Per-source acquisition + parse/normalize/map | feature engineering |
| `core/` | Generic cross-cutting infra (scheduler) | domain logic |
| `entities/` | Country/company lookups and validation | data acquisition |
| `export/` | File export (csv/json/parquet) | caching |
| `features/` | Feature registry, decorators, pipelines, analysis | connector I/O |

## Connector package convention

Each connector package ships four roles:

- `connector.py` — the public class (e.g. `Binance`, `FINNHUB`, `FRED`, ...) exposing
  `async fetch(...)`; owns `_fetch()` acquisition mechanics (HTTP + retries).
- `parser.py` — raw response → structured records (e.g. klines → DataFrame).
- `normalizer.py` — source/record normalization to canonical column layouts.
- `mappings.py` — endpoint tables, series lists, type aliases / literal sets.

Connectors expose their classes from the package root, so
`from hermes.connectors.binance import Binance` works.

## Notes on current gaps (tracked externally)

- `geopolitical_features` is a stub class preserving the public API surface
  (all methods raise `NotImplementedError`) until the GDELT/WGI source rebuild
  lands (checklist Sections 12/13). The old 636-line implementation was removed
  in `137f210`.
- `connectors/gdelt/` currently ships a stub `GDELT` class plus preserved
  `helpers.py` (canonical columns, Doc API URLs) and `mappings.py` (FIPS map).
- `connectors/lib/` now holds only the bundled static datasets used by
  `public_data`. The bundled-dataset move to `data/datasets` is a later section.
- `core/scheduler.py` is intentionally kept in `core/` (decision from Section 1
  review); it is scheduled/imported only by its test.

## Cross-cutting rules

- All connectors default to `cache=RawCache()` when constructed standalone, and
  share the facade-provided cache inside `Hermes`.
- Feature calls are async; `mode="F"` returns latest scalar, `mode="ML"` returns
  a monthly `pd.Series`.
- Import paths use absolute `from hermes.<subsystem>...` imports.