# Hermes Codebase

## Purpose

This document explains the responsibility of every major directory and file inside the Hermes codebase.

Hermes is organized into layers so that:

* public APIs remain stable
* connectors remain source-specific
* acquisition infrastructure is reusable
* parsing and normalization are separate concerns
* schemas define canonical representations
* validation guarantees data quality
* metadata and provenance remain attached to datasets
* storage and querying remain replaceable
* features remain separate from raw data infrastructure

---

# Repository Structure

```text
Hermes/
├── .github/
│   └── workflows/
│       ├── publish.yml
│       └── tests.yml
│
├── docs/
│   ├── architecture/
│   │   ├── overview.md
│   │   ├── connectors.md
│   │   ├── schemas.md
│   │   ├── parsing.md
│   │   ├── normalization.md
│   │   ├── validation.md
│   │   ├── metadata.md
│   │   ├── provenance.md
│   │   ├── storage.md
│   │   ├── querying.md
│   │   ├── versioning.md
│   │   └── entities.md
│   │
│   ├── connectors/
│   │   ├── binance.md
│   │   ├── finnhub.md
│   │   ├── fred.md
│   │   ├── gdelt.md
│   │   ├── imf.md
│   │   ├── opensanctions.md
│   │   ├── sec.md
│   │   ├── world_bank.md
│   │   └── yfinance.md
│   │
│   ├── analysis/
│   │   ├── fundamentals.md
│   │   └── technical.md
│   │
│   └── checklist.md
│
├── hermes/
│   ├── __init__.py
│   ├── constants.py
│   │
│   ├── api/
│   ├── acquisition/
│   ├── connectors/
│   ├── core/
│   ├── schemas/
│   ├── parsing/
│   ├── normalization/
│   ├── validation/
│   ├── metadata/
│   ├── entities/
│   ├── datasets/
│   ├── storage/
│   ├── query/
│   ├── export/
│   └── features/
│
├── data/
│   └── datasets/
│
├── scripts/
│   ├── sync.py
│   ├── validate.py
│   └── profile.py
│
├── tests/
│   ├── conftest.py
│   ├── unit/
│   ├── connectors/
│   ├── features/
│   └── integration/
│
├── .env.example
├── .gitignore
├── .python-version
├── LICENSE.md
├── README.md
├── cmd.sh
├── main.py
├── pyproject.toml
└── uv.lock
```

---

# `hermes/`

This is the main Python package.

Everything that implements Hermes itself belongs here.

The package is divided by responsibility rather than by individual connector.

```text
hermes/
├── api/
├── acquisition/
├── connectors/
├── core/
├── schemas/
├── parsing/
├── normalization/
├── validation/
├── metadata/
├── entities/
├── datasets/
├── storage/
├── query/
├── export/
└── features/
```

The general flow is:

```text
User
 ↓
API
 ↓
Connector / Data Operation
 ↓
Acquisition
 ↓
Parse
 ↓
Normalize
 ↓
Validate
 ↓
Metadata + Provenance
 ↓
Dataset
 ↓
Storage / Query / Export
```

---

# `hermes/__init__.py`

The main public package entry point.

The primary user-facing interface should be exposed here.

Example:

```python
from hermes import Hermes

hr = Hermes()
```

Users should generally not need to import internal Hermes modules directly.

For example, normal usage should not require:

```python
from hermes.normalization.engine import NormalizationEngine
```

The internal architecture can change while the public API remains stable.

---

# `hermes/constants.py`

Contains package-wide constants.

Examples:

```text
default values
supported formats
schema versions
default timeouts
dataset identifiers
common configuration values
```

Constants that belong specifically to one connector should remain inside that connector.

---

# `hermes/api/`

The public API layer.

```text
api/
├── __init__.py
├── acquire.py
├── data.py
├── datasets.py
├── entities.py
├── schemas.py
└── storage.py
```

This layer translates user-facing operations into internal Hermes operations.

It should remain relatively thin.

---

## `api/acquire.py`

Public acquisition operations.

Examples:

```python
hr.fetch(...)
hr.fetch_raw(...)
hr.sync(...)
```

Responsible for coordinating acquisition requests.

It should delegate actual HTTP, caching, pagination, retry, and connector-specific behavior to the appropriate subsystems.

---

## `api/data.py`

General data operations.

Examples:

```python
hr.parse(...)
hr.normalize(...)
hr.transform(...)
hr.validate(...)
```

This is the entry point for working with arbitrary datasets, not necessarily data retrieved through a Hermes connector.

For example:

```python
hr.normalize(my_dataframe)
```

---

## `api/datasets.py`

Public dataset catalog operations.

Examples:

```python
hr.datasets.list()
hr.datasets.get(...)
hr.datasets.search(...)
```

Provides users with a consistent interface for discovering Hermes datasets.

---

## `api/entities.py`

Public entity operations.

Examples:

```python
hr.resolve_entity(...)
hr.resolve_country(...)
hr.resolve_company(...)
```

Delegates entity resolution to the `entities/` subsystem.

---

## `api/schemas.py`

Public schema operations.

Examples:

```python
hr.get_schema(...)
hr.register_schema(...)
hr.compare_schema(...)
hr.migrate(...)
```

Delegates schema operations to the `schemas/` subsystem.

---

## `api/storage.py`

Public persistence operations.

Examples:

```python
hr.save(...)
hr.load(...)
hr.query(...)
hr.materialize(...)
```

Delegates storage operations to the storage and query layers.

---

# `hermes/acquisition/`

Reusable infrastructure for obtaining data.

```text
acquisition/
├── __init__.py
├── client.py
├── cache.py
├── pagination.py
├── retry.py
├── rate_limit.py
└── sync.py
```

This layer should contain generic acquisition mechanisms.

Connectors should use this infrastructure instead of independently implementing the same HTTP, retry, caching, and pagination logic.

---

## `acquisition/client.py`

Common client for communicating with external data sources.

Responsible for things such as:

```text
HTTP requests
headers
timeouts
request handling
response handling
connection configuration
```

Source-specific endpoints remain in connectors.

---

## `acquisition/cache.py`

Caching infrastructure.

Responsible for:

```text
storing responses
retrieving cached responses
cache keys
expiration
cache invalidation
```

The goal is to avoid repeatedly downloading identical data.

---

## `acquisition/pagination.py`

Reusable pagination mechanisms.

Different APIs may use:

```text
page numbers
offsets
cursors
next URLs
date ranges
tokens
```

This module provides reusable pagination machinery.

Source-specific pagination configuration belongs to the connector.

---

## `acquisition/retry.py`

Retry infrastructure.

Responsible for retrying temporary failures.

Examples:

```text
timeouts
temporary server errors
connection failures
rate-limit responses
```

Retry behavior should be configurable.

---

## `acquisition/rate_limit.py`

Rate-limit handling.

Responsible for:

```text
tracking request limits
waiting between requests
handling rate-limit responses
preventing excessive requests
```

---

## `acquisition/sync.py`

Incremental synchronization.

Instead of downloading an entire dataset repeatedly:

```text
Existing:
2020 → 2025

New:
2025 → 2026
```

The synchronization layer determines what data needs to be acquired.

---

# `hermes/connectors/`

Source-specific integrations.

```text
connectors/
├── __init__.py
├── base.py
├── registry.py
├── binance/
├── finnhub/
├── fred/
├── gdelt/
├── imf/
├── opensanctions/
├── sec/
├── world_bank/
└── yfinance/
```

A connector represents one external data source.

Examples:

```text
SEC
FRED
World Bank
IMF
GDELT
Binance
Finnhub
OpenSanctions
Yahoo Finance
```

A connector should contain knowledge specific to that source.

---

## `connectors/base.py`

Defines the common connector interface.

Every connector should follow the same general contract.

Conceptually:

```text
Connector
├── identity
├── capabilities
├── acquisition
├── parsing
├── normalization
├── schema
└── metadata
```

This allows the rest of Hermes to interact with connectors consistently.

---

## `connectors/registry.py`

Registry of available connectors.

Conceptually:

```text
"sec" → SEC connector
"fred" → FRED connector
"world_bank" → World Bank connector
```

The registry allows Hermes to discover and retrieve connectors dynamically.

---

# Connector Structure

Each connector follows the same basic structure:

```text
source/
├── __init__.py
├── connector.py
├── parser.py
├── normalizer.py
└── mappings.py
```

Some connectors may contain additional source-specific modules.

---

## `connector.py`

The source integration itself.

Responsible for coordinating:

```text
source endpoints
parameters
requests
acquisition
pagination
parser
normalizer
dataset/schema selection
```

It should not become a giant file containing every piece of source-specific logic.

---

## `parser.py`

Converts the source's raw representation into structured records.

Example:

```text
Raw API response
        ↓
      Parser
        ↓
Structured records
```

The parser understands the source's response format.

It does not decide the final Hermes meaning of every field.

---

## `normalizer.py`

Handles source-specific semantic normalization.

Example:

```text
Source:
us-gaap:Revenues

        ↓

Hermes:
financial.revenue
```

Source-specific mappings belong here or in `mappings.py`.

Generic normalization rules belong in `hermes/normalization/`.

---

## `mappings.py`

Contains mappings between source concepts and Hermes concepts.

Examples:

```text
source field → Hermes field
source identifier → Hermes identifier
source unit → Hermes unit
source category → Hermes category
```

This is particularly important for sources with inconsistent or complicated vocabularies.

---

# `connectors/sec/`

SEC-specific implementation.

```text
sec/
├── __init__.py
├── connector.py
├── parser.py
├── normalizer.py
├── mappings.py
└── tags.py
```

---

## `sec/tags.py`

SEC-specific taxonomy/tag knowledge.

For example:

```text
us-gaap tags
company concepts
filing concepts
taxonomy mappings
```

SEC-specific concepts should not pollute the global normalization engine.

---

# `connectors/gdelt/`

GDELT-specific implementation.

```text
gdelt/
├── __init__.py
├── connector.py
├── parser.py
├── normalizer.py
├── mappings.py
└── helpers.py
```

`helpers.py` contains GDELT-specific utilities that do not belong in generic Hermes infrastructure.

---

# `hermes/core/`

Fundamental Hermes objects.

```text
core/
├── __init__.py
├── dataset.py
├── result.py
├── metadata.py
├── provenance.py
├── lineage.py
└── versioning.py
```

These represent concepts that are fundamental to Hermes itself.

---

## `core/dataset.py`

Defines the Hermes Dataset abstraction.

A Hermes dataset should eventually represent more than a raw DataFrame.

Conceptually:

```text
Dataset
├── data
├── schema
├── metadata
├── provenance
├── lineage
├── quality
└── version
```

The dataset is the central object produced by Hermes operations.

---

## `core/result.py`

Standardized results from Hermes operations.

Can represent:

```text
success
warning
partial
failure
```

Useful for ingestion jobs and multi-source operations.

---

## `core/metadata.py`

Defines the core metadata representation.

It describes what metadata looks like inside Hermes.

The actual extraction of metadata belongs to `metadata/extractor.py`.

---

## `core/provenance.py`

Defines provenance information.

Provenance answers:

> Where did this data come from?

Examples:

```text
source
URL/API
retrieval time
source dataset
source version
request information
```

---

## `core/lineage.py`

Defines transformation lineage.

Lineage answers:

> What happened to the data after Hermes obtained it?

Example:

```text
Source
 ↓
Raw data
 ↓
Parsed
 ↓
Normalized
 ↓
Validated
 ↓
Transformed
 ↓
Stored
```

---

## `core/versioning.py`

Defines version information for datasets and related artifacts.

Examples:

```text
dataset version
schema version
transformation version
snapshot version
```

---

# `hermes/schemas/`

Canonical Hermes schemas.

```text
schemas/
├── __init__.py
├── base.py
├── registry.py
├── entity.py
├── document.py
├── economic.py
├── financial.py
├── market.py
├── geopolitical.py
└── security.py
```

Schemas define how normalized Hermes data should look.

The goal is interoperability between different sources.

Example:

```text
Source A
   ↓
Mapping
   ↓
Hermes Schema

Source B
   ↓
Mapping
   ↓
Same Hermes Schema
```

---

## `schemas/base.py`

Base schema functionality.

Defines common schema behavior such as:

```text
field definitions
types
constraints
schema identity
schema version
```

---

## `schemas/registry.py`

Schema registry.

Responsible for registering and retrieving Hermes schemas.

Conceptually:

```text
financial.v1
economic.v1
market.v1
```

---

## `schemas/entity.py`

Schema definitions for entities.

Examples:

```text
company
country
organization
person
location
```

---

## `schemas/document.py`

Schemas for document-like data.

Examples:

```text
filings
articles
reports
documents
events
```

---

## `schemas/economic.py`

Canonical economic data structures.

Examples:

```text
GDP
inflation
unemployment
interest rates
trade
economic indicators
```

---

## `schemas/financial.py`

Canonical financial data structures.

Examples:

```text
revenue
assets
liabilities
equity
profit
cash flow
financial statements
```

---

## `schemas/market.py`

Market data structures.

Examples:

```text
OHLCV
trades
order books
quotes
market statistics
```

---

## `schemas/geopolitical.py`

Geopolitical data structures.

Examples:

```text
events
countries
relationships
conflicts
political events
geopolitical indicators
```

---

## `schemas/security.py`

Security-related data structures.

Examples:

```text
sanctions
military data
security events
threat information
```

---

# `hermes/parsing/`

Generic parsing infrastructure.

```text
parsing/
├── __init__.py
├── engine.py
├── records.py
└── errors.py
```

Parsing answers:

> How do we turn a source representation into structured records?

---

## `parsing/engine.py`

Generic parsing engine.

Coordinates parser execution and common parsing behavior.

---

## `parsing/records.py`

Defines intermediate record representations.

The intermediate representation sits between:

```text
raw source data
```

and:

```text
canonical Hermes data
```

---

## `parsing/errors.py`

Parsing-specific errors.

Examples:

```text
invalid response
malformed record
unsupported format
missing required structure
```

---

# `hermes/normalization/`

Generic normalization infrastructure.

```text
normalization/
├── __init__.py
├── engine.py
├── mapping.py
├── rules.py
└── errors.py
```

Normalization answers:

> How do we make structurally different data consistent?

Examples:

```text
2026/01/01
    ↓
2026-01-01
```

```text
"1,234.50"
    ↓
1234.50
```

```text
Pakistan
PK
PAK
    ↓
canonical country representation
```

---

## `normalization/engine.py`

Runs normalization pipelines.

Coordinates normalization rules and mappings.

---

## `normalization/mapping.py`

Generic mapping infrastructure.

Used to map source values into canonical representations.

---

## `normalization/rules.py`

Reusable normalization rules.

Examples:

```text
date normalization
timestamp normalization
numeric conversion
string cleanup
unit conversion
null normalization
identifier normalization
```

---

## `normalization/errors.py`

Normalization-specific errors.

---

# `hermes/validation/`

Data quality and correctness validation.

```text
validation/
├── __init__.py
├── engine.py
├── checks.py
├── contracts.py
├── reports.py
└── errors.py
```

Validation answers:

> Can Hermes trust that this dataset satisfies its expected structure and quality requirements?

---

## `validation/engine.py`

Runs validation checks against datasets.

---

## `validation/checks.py`

Individual validation checks.

Examples:

```text
null checks
duplicate checks
type checks
range checks
date checks
schema checks
identifier checks
integrity checks
```

---

## `validation/contracts.py`

Defines expectations for datasets.

For example:

```text
required fields
allowed types
required identifiers
constraints
relationships
```

---

## `validation/reports.py`

Produces structured validation and quality reports.

Example:

```text
Rows: 100,000

Schema:
✓ valid

Types:
✓ valid

Duplicates:
⚠ 124 duplicates

Missing values:
✓ acceptable

Date range:
✓ valid
```

---

## `validation/errors.py`

Validation-specific errors.

---

# `hermes/metadata/`

Metadata discovery and extraction.

```text
metadata/
├── __init__.py
├── extractor.py
├── models.py
└── registry.py
```

This subsystem determines metadata from datasets.

---

## `metadata/extractor.py`

Extracts metadata automatically.

Potential metadata:

```text
row count
column count
column names
data types
null counts
unique counts
date range
frequency
duplicates
source
schema
quality information
```

---

## `metadata/models.py`

Defines metadata models.

---

## `metadata/registry.py`

Registry for metadata definitions and metadata-related extensions.

---

# `hermes/entities/`

Entity resolution and canonical entity management.

```text
entities/
├── __init__.py
├── registry.py
├── resolver.py
├── models.py
├── aliases.py
├── countries.py
└── companies.py
```

This subsystem answers:

> What real-world entity does this record refer to?

Example:

```text
Apple Inc.
Apple Computer Inc.
Apple
AAPL
US0378331005
```

may represent the same company.

Likewise:

```text
Pakistan
PK
PAK
586
```

may represent the same country.

---

## `entities/registry.py`

Registry of known entities.

---

## `entities/resolver.py`

Entity resolution engine.

Responsible for matching source representations to canonical Hermes entities.

---

## `entities/models.py`

Entity models.

---

## `entities/aliases.py`

Known aliases and alternative names.

---

## `entities/countries.py`

Country-specific entity data and mappings.

---

## `entities/companies.py`

Company-specific entity data and mappings.

---

# `hermes/datasets/`

Dataset catalog and registry.

```text
datasets/
├── __init__.py
├── registry.py
├── catalog.py
└── models.py
```

This subsystem manages datasets as first-class Hermes resources.

---

## `datasets/registry.py`

Dataset registry.

Keeps track of datasets available to Hermes.

---

## `datasets/catalog.py`

Dataset discovery and catalog operations.

Supports functionality such as:

```python
hr.datasets.list()
hr.datasets.search(...)
hr.datasets.get(...)
```

---

## `datasets/models.py`

Dataset catalog models.

Potential fields include:

```text
dataset ID
name
description
source
schema
coverage
frequency
version
quality
update information
```

---

# `hermes/storage/`

Persistence abstraction.

```text
storage/
├── __init__.py
├── base.py
├── filesystem.py
├── parquet.py
└── duckdb.py
```

Storage answers:

> Where should Hermes persist datasets?

The rest of Hermes should not be tightly coupled to one storage backend.

---

## `storage/base.py`

Defines the storage interface.

Potential operations:

```text
save
load
delete
exists
list
```

---

## `storage/filesystem.py`

Filesystem-based storage implementation.

---

## `storage/parquet.py`

Parquet-specific storage implementation.

---

## `storage/duckdb.py`

DuckDB storage/query integration.

---

# `hermes/query/`

Query engine.

```text
query/
├── __init__.py
├── engine.py
├── filters.py
└── expressions.py
```

Provides structured access to stored Hermes datasets.

---

## `query/engine.py`

Executes queries.

---

## `query/filters.py`

Defines filtering operations.

Examples:

```text
country == "PAK"
date >= ...
revenue > ...
```

---

## `query/expressions.py`

Defines query expressions and composable query logic.

---

# `hermes/export/`

Data export.

```text
export/
├── __init__.py
├── csv.py
├── json.py
├── parquet.py
└── arrow.py
```

Allows Hermes datasets to integrate with external ecosystems.

---

## `export/csv.py`

CSV export.

---

## `export/json.py`

JSON export.

---

## `export/parquet.py`

Parquet export.

---

## `export/arrow.py`

Apache Arrow export.

Arrow is particularly important because it allows Hermes data to integrate efficiently with tools such as:

```text
Pandas
Polars
DuckDB
PyArrow
ML pipelines
```

---

# `hermes/features/`

Derived analytical features.

```text
features/
├── __init__.py
├── registry.py
├── decorator.py
├── financial/
└── country_risk/
```

Features are derived from datasets rather than being raw source data.

General flow:

```text
Raw Data
   ↓
Canonical Dataset
   ↓
Feature Pipeline
   ↓
Derived Features
```

---

## `features/registry.py`

Feature registry.

Allows Hermes to discover available feature definitions.

---

## `features/decorator.py`

Provides decorators or registration mechanisms for defining features.

---

# `features/financial/`

Financial feature implementations.

```text
financial/
├── __init__.py
├── crypto.py
├── fundamental.py
├── stocks.py
├── technical.py
└── filing.py
```

Examples:

```text
technical indicators
fundamental features
stock features
crypto features
filing-derived features
```

---

# `features/country_risk/`

Country-risk feature pipeline.

```text
country_risk/
├── __init__.py
├── economic.py
├── environmental.py
├── geopolitical.py
├── security.py
├── social.py
└── pipeline.py
```

Separates country-risk feature calculations by domain.

---

# `data/`

Local project data.

```text
data/
└── datasets/
```

This should contain datasets that Hermes intentionally ships with or uses for local functionality.

Examples:

```text
CRS
CVS
FSI
CPI
HDI
HRS
NATO
SIPRI
```

Large external datasets should not automatically be committed to the Git repository.

---

# `scripts/`

Developer and maintenance scripts.

```text
scripts/
├── sync.py
├── validate.py
└── profile.py
```

---

## `scripts/sync.py`

Runs dataset synchronization jobs.

Used for maintaining local or packaged datasets.

---

## `scripts/validate.py`

Runs validation operations over datasets.

Useful during development and CI.

---

## `scripts/profile.py`

Runs profiling operations to understand dataset characteristics.

Useful for:

```text
schema discovery
data quality analysis
performance analysis
dataset profiling
```

---

# `tests/`

All automated tests.

```text
tests/
├── conftest.py
├── unit/
├── connectors/
├── features/
└── integration/
```

Tests should mirror the architecture.

---

# `tests/conftest.py`

Shared pytest fixtures and test configuration.

Examples:

```text
test datasets
mock responses
temporary storage
connector fixtures
common configuration
```

---

# `tests/unit/`

Tests individual components independently.

```text
unit/
├── acquisition/
├── parsing/
├── normalization/
├── validation/
├── metadata/
├── entities/
├── schemas/
├── storage/
└── query/
```

Unit tests should avoid depending on real external APIs.

---

# `tests/connectors/`

Connector-specific tests.

```text
connectors/
├── test_binance.py
├── test_finnhub.py
├── test_fred.py
├── test_gdelt.py
├── test_imf.py
├── test_opensanctions.py
├── test_sec.py
├── test_world_bank.py
└── test_yfinance.py
```

These verify that each connector correctly:

```text
acquires
parses
normalizes
maps
and produces
```

the expected Hermes dataset.

---

# `tests/features/`

Tests feature implementations.

Examples:

```text
economic
environmental
financial
fundamental
geopolitical
security
social
technical
pipeline
```

Feature tests should verify formulas and expected outputs.

---

# `tests/integration/`

Tests multiple Hermes components working together.

```text
integration/
├── test_pipeline.py
├── test_storage.py
└── test_end_to_end.py
```

Examples:

```text
connector
 ↓
parse
 ↓
normalize
 ↓
validate
 ↓
metadata
 ↓
dataset
 ↓
storage
```

---

# `.github/workflows/`

CI/CD automation.

```text
.github/
└── workflows/
    ├── publish.yml
    └── tests.yml
```

---

## `tests.yml`

Runs automated tests and quality checks.

Potential checks:

```text
unit tests
integration tests
linting
type checking
package build
```

---

## `publish.yml`

Responsible for package publishing.

Should only publish versions that pass the required CI checks.

---

# `docs/`

Project documentation.

```text
docs/
├── architecture/
├── connectors/
├── analysis/
└── checklist.md
```

Documentation should explain both how Hermes works and how contributors should extend it.

---

# `docs/architecture/`

Internal architecture documentation.

Each file explains one subsystem:

```text
overview.md
connectors.md
schemas.md
parsing.md
normalization.md
validation.md
metadata.md
provenance.md
storage.md
querying.md
versioning.md
entities.md
```

These documents should describe **design decisions and contracts**, not merely repeat implementation details.

---

# `docs/connectors/`

Connector-specific documentation.

Each connector should document:

```text
source
coverage
authentication requirements
available datasets
API limitations
rate limits
pagination
raw format
parsing behavior
normalization mappings
canonical schemas
known limitations
```

---

# `docs/analysis/`

Documentation for analytical feature systems.

Examples:

```text
fundamentals.md
technical.md
```

These documents should explain feature definitions, formulas, assumptions, and expected inputs/outputs.

---

# `docs/checklist.md`

Engineering checklist for Hermes development.

This should be used to track whether major platform capabilities and connector requirements have been implemented.

---

# `README.md`

Primary public introduction to Hermes.

Should explain:

```text
what Hermes is
why it exists
installation
basic usage
supported sources
basic examples
links to documentation
```

The README should remain focused on users and contributors rather than exposing every internal implementation detail.

---

# `pyproject.toml`

Python project configuration.

Contains things such as:

```text
package metadata
dependencies
development dependencies
build configuration
tool configuration
test configuration
lint configuration
type checking
```

This is the main Python project configuration file.

---

# `uv.lock`

Locked dependency versions generated and maintained by `uv`.

Provides reproducible environments.

It should normally be updated through `uv`, not manually edited.

---

# `.python-version`

Defines the Python version expected by the project.

---

# `.env.example`

Example environment configuration.

It should contain variable names and examples, but never real secrets.

---

# `.gitignore`

Files and directories that should not be committed.

Examples:

```text
cache
virtual environments
local secrets
temporary files
build artifacts
```

---

# `LICENSE.md`

Project license.

Defines how Hermes can be used, modified, and distributed.

---

# `cmd.sh`

Project helper shell commands.

Can provide shortcuts for common developer operations such as:

```text
tests
lint
format
build
publish
development commands
```

---

# `main.py`

Development/demo entry point if needed.

This should not contain the Hermes core architecture.

Production library functionality belongs under:

```text
hermes/
```

---

# Architectural Boundaries

The most important rule in the codebase is that responsibilities should not leak between layers.

## Connector

Knows:

```text
source-specific API
source-specific format
source-specific concepts
source-specific mappings
```

Does not own generic:

```text
retry
cache
storage
validation engine
```

---

## Acquisition

Knows:

```text
how to reliably retrieve data
```

Does not know what:

```text
GDP
revenue
country
sanction
```

means.

---

## Parser

Knows:

```text
how to interpret the source representation
```

Does not define the final canonical meaning.

---

## Normalizer

Knows:

```text
how to make data consistent
```

Generic normalization belongs globally.

Source-specific semantic mapping belongs to connectors.

---

## Schema

Defines:

```text
what canonical Hermes data should look like
```

---

## Validation

Determines:

```text
whether data satisfies expected requirements
```

---

## Metadata

Describes:

```text
what the dataset contains
```

---

## Provenance

Describes:

```text
where the dataset came from
```

---

## Lineage

Describes:

```text
what happened to the dataset
```

---

## Storage

Answers:

```text
where the dataset is persisted
```

---

## Query

Answers:

```text
how stored datasets are accessed
```

---

## Export

Answers:

```text
how Hermes data is transferred into external formats/tools
```

---

## Features

Answers:

```text
what useful information can be derived from canonical data
```

---

# Data Flow

A typical connector pipeline should conceptually look like:

```text
External Source
      ↓
Connector
      ↓
Acquisition
      ↓
Raw Response
      ↓
Parser
      ↓
Structured Records
      ↓
Source Mapping
      ↓
Normalization
      ↓
Canonical Hermes Schema
      ↓
Validation
      ↓
Metadata
      ↓
Provenance
      ↓
Lineage
      ↓
Hermes Dataset
      ↓
┌──────────┬──────────┬──────────┐
↓          ↓          ↓
Storage    Query      Export
```

Features can then consume canonical datasets:

```text
Hermes Dataset
      ↓
Feature Pipeline
      ↓
Derived Dataset
```

---

# Development Rule

When adding a new capability, place it in the layer responsible for that capability.

Do not solve a global problem inside a connector.

Do not solve a source-specific problem inside global infrastructure.

The general rule is:

```text
Generic behavior
    → Hermes subsystem

Source-specific behavior
    → Connector

Canonical meaning
    → Schema

Derived analytical behavior
    → Features
```

This separation is what allows Hermes to grow from a collection of connectors into a maintainable data platform.
