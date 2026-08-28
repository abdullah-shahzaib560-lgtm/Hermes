# Hermes — Internal Engineering Tasks

## 0. Project Direction

**Objective:** Evolve Hermes from a collection of data-source connectors into a serious, reusable data platform/SDK that can:

* Acquire data
* Preserve raw data
* Parse source-specific formats
* Normalize heterogeneous data into canonical Hermes schemas
* Validate data
* Profile and describe datasets
* Attach metadata
* Track provenance and lineage
* Resolve entities
* Register and version datasets/schemas
* Store and query data
* Export data
* Synchronize incremental updates
* Provide derived feature pipelines

### Core principle

```text
External Source
      ↓
   Connector
      ↓
  Raw Data
      ↓
    Parse
      ↓
 Normalize
      ↓
  Validate
      ↓
 Metadata + Provenance + Lineage
      ↓
 Hermes Dataset
      ↓
 Storage / Query / Export / Features
```

---

# 1. Repository Refactor

* [ ] Refactor current repository toward the new architecture.
* [ ] Rename `hermes/sources/` → `hermes/connectors/`.
* [ ] Reduce the responsibility of `hermes/core/`.
* [ ] Move acquisition infrastructure out of `core/`.
* [ ] Move country/entity functionality into `entities/`.
* [ ] Move feature infrastructure into `features/`.
* [ ] Remove `core/helper.py`.
* [ ] Move functionality from `helper.py` into the appropriate subsystem.
* [ ] Separate data infrastructure from feature engineering.
* [ ] Create architecture documentation.
* [ ] Preserve existing public API behavior where possible.
* [ ] Run the existing test suite before and after each major refactor.

---

# 2. Core Dataset System

### Create

```text
hermes/core/
├── dataset.py
├── result.py
├── metadata.py
├── provenance.py
├── lineage.py
└── versioning.py
```

### Tasks

* [ ] Create `Dataset` abstraction.
* [ ] Define dataset identity.
* [ ] Define dataset name.
* [ ] Define dataset ID.
* [ ] Define dataset schema reference.
* [ ] Define dataset version.
* [ ] Define dataset metadata reference.
* [ ] Define provenance reference.
* [ ] Define lineage reference.
* [ ] Create standardized operation/result objects.
* [ ] Create standardized error handling.
* [ ] Ensure datasets are independent of specific storage engines.

---

# 3. Canonical Schema System

### Create

```text
hermes/schemas/
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

### Tasks

* [ ] Define what a Hermes canonical schema is.
* [ ] Define schema fields.
* [ ] Define field types.
* [ ] Define required fields.
* [ ] Define optional fields.
* [ ] Define primary keys.
* [ ] Define foreign/entity references.
* [ ] Define units.
* [ ] Define temporal semantics.
* [ ] Define allowed values where necessary.
* [ ] Define schema versions.
* [ ] Create base schema contract.
* [ ] Create schema registry.
* [ ] Implement schema registration.
* [ ] Implement schema retrieval.
* [ ] Implement schema comparison.
* [ ] Implement schema compatibility checking.
* [ ] Implement schema versioning.
* [ ] Implement schema migration framework.

### Initial canonical schemas

* [ ] Entity
* [ ] Economic observation
* [ ] Financial observation
* [ ] Market observation
* [ ] Geopolitical event
* [ ] Security event
* [ ] Document

---

# 4. Parsing System

### Create

```text
hermes/parsing/
├── engine.py
├── records.py
└── errors.py
```

### Tasks

* [ ] Define parser contract.
* [ ] Support JSON.
* [ ] Support CSV.
* [ ] Support nested JSON.
* [ ] Support lists of records.
* [ ] Support tabular data.
* [ ] Support XML where required.
* [ ] Preserve source fields.
* [ ] Preserve raw values.
* [ ] Handle malformed records.
* [ ] Define parser errors.
* [ ] Define parser warnings.
* [ ] Allow connector-specific parsers.
* [ ] Keep source-specific parsing logic inside connectors.
* [ ] Prevent the generic parser from containing SEC/GDELT/etc. business logic.

---

# 5. Normalization System

### Create

```text
hermes/normalization/
├── engine.py
├── mapping.py
├── rules.py
└── errors.py
```

### Tasks

* [ ] Define normalization contract.
* [ ] Define source → canonical field mapping.
* [ ] Define semantic concept mappings.
* [ ] Define type conversion.
* [ ] Define date normalization.
* [ ] Define timestamp normalization.
* [ ] Define country-code normalization.
* [ ] Define company/entity identifier normalization.
* [ ] Define unit normalization.
* [ ] Define currency normalization.
* [ ] Define missing-value normalization.
* [ ] Define duplicate handling.
* [ ] Define normalization warnings.
* [ ] Define normalization errors.
* [ ] Implement normalization engine.
* [ ] Implement reusable normalization rules.
* [ ] Allow connector-specific mappings.
* [ ] Ensure normalization does not contain source acquisition logic.

### Example responsibility

```text
SEC:
us-gaap:Revenues
        ↓
Hermes:
revenue
```

```text
World Bank:
Country Name
        ↓
Hermes:
entity_id
```

```text
GDELT:
Actor1CountryCode
        ↓
Hermes:
actor_1_entity_id
```

---

# 6. Validation System

### Create

```text
hermes/validation/
├── engine.py
├── checks.py
├── contracts.py
├── reports.py
└── errors.py
```

### Tasks

* [ ] Create validation engine.
* [ ] Schema validation.
* [ ] Type validation.
* [ ] Required-field validation.
* [ ] Null validation.
* [ ] Range validation.
* [ ] Date validation.
* [ ] Duplicate validation.
* [ ] Primary-key validation.
* [ ] Foreign-key validation.
* [ ] Referential-integrity validation.
* [ ] Unit validation.
* [ ] Constraint validation.
* [ ] Create `ValidationReport`.
* [ ] Separate errors from warnings.
* [ ] Implement `validate()`.
* [ ] Implement `check_quality()`.
* [ ] Implement `check_completeness()`.
* [ ] Implement `check_freshness()`.
* [ ] Implement `check_integrity()`.

---

# 7. Metadata System

### Create

```text
hermes/metadata/
├── extractor.py
├── models.py
└── registry.py
```

### Tasks

* [ ] Create metadata model.
* [ ] Dataset-level metadata.
* [ ] Column-level metadata.
* [ ] Data type metadata.
* [ ] Row count.
* [ ] Column count.
* [ ] Null statistics.
* [ ] Unique statistics.
* [ ] Date range.
* [ ] Frequency detection.
* [ ] Entity coverage.
* [ ] Source information.
* [ ] Retrieval timestamp.
* [ ] Last observation timestamp.
* [ ] Expected update frequency.
* [ ] Quality information.
* [ ] Implement `get_metadata()`.
* [ ] Implement `inspect()`.
* [ ] Implement `profile()`.

---

# 8. Provenance System

### Tasks

* [ ] Define provenance model.
* [ ] Record source.
* [ ] Record source URL/API endpoint.
* [ ] Record retrieval timestamp.
* [ ] Record connector.
* [ ] Record connector version.
* [ ] Record raw-data checksum.
* [ ] Record parser version.
* [ ] Record normalizer version.
* [ ] Record schema version.
* [ ] Record validation result.
* [ ] Record transformation information.
* [ ] Implement `get_provenance()`.
* [ ] Make provenance immutable once recorded where appropriate.

---

# 9. Lineage System

### Tasks

* [ ] Define lineage model.
* [ ] Track input dataset.
* [ ] Track output dataset.
* [ ] Track operations.
* [ ] Track transformations.
* [ ] Track timestamps.
* [ ] Track versions.
* [ ] Track parameters.
* [ ] Build dataset lineage graph.
* [ ] Implement `get_lineage()`.
* [ ] Make lineage queryable.

### Target

```text
Source
  ↓
Raw Dataset
  ↓
Parsed Dataset
  ↓
Normalized Dataset
  ↓
Validated Dataset
  ↓
Stored Dataset
  ↓
Feature Dataset
```

---

# 10. Acquisition System

### Create

```text
hermes/acquisition/
├── client.py
├── cache.py
├── pagination.py
├── retry.py
├── rate_limit.py
└── sync.py
```

### Tasks

* [ ] Move current cache implementation.
* [ ] Move retry logic.
* [ ] Move pagination logic.
* [ ] Create common HTTP client.
* [ ] Create rate-limit handling.
* [ ] Create request timeout handling.
* [ ] Create resumable acquisition.
* [ ] Create sync state.
* [ ] Track last successful synchronization.
* [ ] Track source cursors.
* [ ] Track source timestamps.
* [ ] Implement `fetch_raw()`.
* [ ] Implement `sync()`.
* [ ] Preserve existing `_fetch()` abstraction.
* [ ] Keep `_fetch()` responsible for source acquisition mechanics.

---

# 11. Connector Architecture

### Create

```text
hermes/connectors/
├── base.py
└── registry.py
```

### Define connector responsibilities

```text
_fetch()
    ↓
fetch_raw()
    ↓
parse()
    ↓
normalize()
    ↓
validate()
```

### Tasks

* [ ] Define `BaseConnector`.
* [ ] Define connector lifecycle.
* [ ] Define connector metadata.
* [ ] Define connector capabilities.
* [ ] Define connector schema declaration.
* [ ] Define connector configuration.
* [ ] Create connector registry.
* [ ] Add connector discovery.
* [ ] Add connector enable/disable capability.
* [ ] Standardize connector errors.
* [ ] Standardize connector logging.

---

# 12. Connector Refactor

Refactor each connector into the standard architecture.

### Binance

* [ ] `connector.py`
* [ ] `parser.py`
* [ ] `normalizer.py`
* [ ] `mappings.py`

### Finnhub

* [ ] `connector.py`
* [ ] `parser.py`
* [ ] `normalizer.py`
* [ ] `mappings.py`

### FRED

* [ ] `connector.py`
* [ ] `parser.py`
* [ ] `normalizer.py`
* [ ] `mappings.py`

### GDELT

* [ ] `connector.py`
* [ ] `parser.py`
* [ ] `normalizer.py`
* [ ] `mappings.py`
* [ ] `helpers.py`

### IMF

* [ ] `connector.py`
* [ ] `parser.py`
* [ ] `normalizer.py`
* [ ] `mappings.py`

### OpenSanctions

* [ ] `connector.py`
* [ ] `parser.py`
* [ ] `normalizer.py`
* [ ] `mappings.py`

### SEC

* [ ] `connector.py`
* [ ] `parser.py`
* [ ] `normalizer.py`
* [ ] `mappings.py`
* [ ] `tags.py`

### World Bank

* [ ] `connector.py`
* [ ] `parser.py`
* [ ] `normalizer.py`
* [ ] `mappings.py`

### YFinance

* [ ] `connector.py`
* [ ] `parser.py`
* [ ] `normalizer.py`
* [ ] `mappings.py`

---

# 13. Reference Connector

Use **World Bank** as the first complete implementation.

* [ ] Refactor World Bank connector.
* [ ] Implement raw acquisition.
* [ ] Implement parsing.
* [ ] Implement canonical mapping.
* [ ] Implement normalization.
* [ ] Implement schema.
* [ ] Implement validation.
* [ ] Implement metadata.
* [ ] Implement provenance.
* [ ] Implement lineage.
* [ ] Test complete pipeline.
* [ ] Document it as the reference connector.
* [ ] Use it as the template for subsequent connectors.

---

# 14. Entity System

### Create

```text
hermes/entities/
├── registry.py
├── resolver.py
├── models.py
├── aliases.py
├── countries.py
└── companies.py
```

### Country

* [ ] Canonical country IDs.
* [ ] ISO-2 resolution.
* [ ] ISO-3 resolution.
* [ ] Country-name resolution.
* [ ] Numeric-code resolution.
* [ ] Country aliases.
* [ ] Historical/source-specific country identifiers.
* [ ] Implement `resolve_country()`.

### Company

* [ ] Canonical company IDs.
* [ ] Company-name resolution.
* [ ] Ticker resolution.
* [ ] CIK resolution.
* [ ] LEI resolution.
* [ ] ISIN support.
* [ ] Source-specific IDs.
* [ ] Company aliases.
* [ ] Implement `resolve_company()`.

### General

* [ ] Implement entity registry.
* [ ] Implement entity aliases.
* [ ] Implement entity resolution.
* [ ] Implement `resolve_entity()`.
* [ ] Connect entities to canonical schemas.

---

# 15. Dataset Catalog

### Create

```text
hermes/datasets/
├── registry.py
├── catalog.py
└── models.py
```

### Tasks

* [ ] Define dataset registry.
* [ ] Define dataset identifier.
* [ ] Define dataset description.
* [ ] Define dataset owner/source.
* [ ] Define dataset schema.
* [ ] Define dataset versions.
* [ ] Define dataset coverage.
* [ ] Define dataset frequency.
* [ ] Define dataset quality.
* [ ] Define dataset freshness.
* [ ] Define dataset provenance.
* [ ] Implement `datasets.list()`.
* [ ] Implement `datasets.get()`.
* [ ] Implement `datasets.search()`.

---

# 16. Storage

### Create

```text
hermes/storage/
├── base.py
├── filesystem.py
├── parquet.py
└── duckdb.py
```

### Tasks

* [ ] Define storage abstraction.
* [ ] Implement filesystem backend.
* [ ] Implement Parquet backend.
* [ ] Integrate DuckDB.
* [ ] Define dataset layout.
* [ ] Define partitioning strategy.
* [ ] Define compression strategy.
* [ ] Define dataset manifests.
* [ ] Store metadata.
* [ ] Store provenance.
* [ ] Store schema information.
* [ ] Store version information.
* [ ] Implement `save()`.
* [ ] Implement `load()`.
* [ ] Implement atomic writes.
* [ ] Add corruption protection.
* [ ] Add storage tests.

---

# 17. Query Engine

### Create

```text
hermes/query/
├── engine.py
├── filters.py
└── expressions.py
```

### Tasks

* [ ] Define query abstraction.
* [ ] Dataset filtering.
* [ ] Column selection.
* [ ] Entity filtering.
* [ ] Date filtering.
* [ ] Range filtering.
* [ ] Sorting.
* [ ] Aggregation.
* [ ] Joins.
* [ ] DuckDB execution.
* [ ] Implement `query()`.
* [ ] Add query tests.

---

# 18. Materialization

### Tasks

* [ ] Define materialization abstraction.
* [ ] Materialize to Polars.
* [ ] Materialize to Pandas.
* [ ] Materialize to Arrow.
* [ ] Materialize to DuckDB relation.
* [ ] Implement `materialize()`.
* [ ] Ensure materialization doesn't mutate canonical data.

---

# 19. Export

### Create

```text
hermes/export/
├── csv.py
├── json.py
├── parquet.py
└── arrow.py
```

### Tasks

* [ ] CSV export.
* [ ] JSON export.
* [ ] Parquet export.
* [ ] Arrow export.
* [ ] Preserve metadata where possible.
* [ ] Preserve schema information.
* [ ] Preserve provenance information where supported.

---

# 20. Dataset Versioning

### Tasks

* [ ] Define dataset version identity.
* [ ] Implement content hashing.
* [ ] Implement schema hashing.
* [ ] Track transformation versions.
* [ ] Create deterministic version IDs.
* [ ] Implement immutable snapshots.
* [ ] Implement `version()`.
* [ ] Implement `snapshot()`.
* [ ] Implement `diff()`.
* [ ] Detect added rows.
* [ ] Detect removed rows.
* [ ] Detect changed rows.
* [ ] Detect schema changes.
* [ ] Add versioning tests.

---

# 21. Schema Migration

### Tasks

* [ ] Define migration model.
* [ ] Define migration registry.
* [ ] Define migration direction.
* [ ] Define compatibility rules.
* [ ] Detect breaking schema changes.
* [ ] Implement forward migrations.
* [ ] Implement `migrate()`.
* [ ] Record migration provenance.
* [ ] Test migration reproducibility.

---

# 22. Public API

### Create

```text
hermes/api/
├── acquire.py
├── data.py
├── datasets.py
├── entities.py
├── schemas.py
└── storage.py
```

### Public API

```python
hr.fetch()
hr.fetch_raw()
hr.sync()

hr.inspect()
hr.get_metadata()
hr.profile()

hr.parse()
hr.normalize()
hr.transform()

hr.validate()
hr.check_quality()
hr.check_completeness()
hr.check_freshness()
hr.check_integrity()

hr.resolve_entity()
hr.resolve_country()
hr.resolve_company()

hr.datasets.list()
hr.datasets.get()
hr.datasets.search()

hr.save()
hr.load()
hr.query()
hr.materialize()

hr.get_provenance()
hr.get_lineage()

hr.version()
hr.snapshot()
hr.diff()

hr.get_schema()
hr.register_schema()
hr.compare_schema()
hr.migrate()
```

### Tasks

* [ ] Keep public API thin.
* [ ] Route API calls to internal engines.
* [ ] Avoid business logic inside API wrappers.
* [ ] Maintain consistent return types.
* [ ] Maintain consistent error behavior.
* [ ] Document public API.
* [ ] Add public API tests.

---

# 23. Feature System

### Preserve

```text
hermes/features/
├── registry.py
├── decorator.py
├── financial/
└── country_risk/
```

### Tasks

* [ ] Move feature registry.
* [ ] Move feature decorator.
* [ ] Refactor financial features.
* [ ] Refactor country-risk features.
* [ ] Make features consume canonical Hermes datasets.
* [ ] Remove source-specific assumptions.
* [ ] Add feature metadata.
* [ ] Add feature versioning.
* [ ] Add feature provenance.
* [ ] Add feature tests.
* [ ] Keep feature engineering separate from core data acquisition.

---

# 24. Static Data

Move current bundled datasets into:

```text
data/
└── datasets/
    ├── crs.csv
    ├── cvs.csv
    ├── fsi.csv
    ├── global_cpi_all.csv
    ├── hdi1.csv
    ├── hrs.csv
    ├── nato.csv
    └── sipri.csv
```

### Tasks

* [ ] Register each dataset.
* [ ] Create metadata for each dataset.
* [ ] Define schema for each dataset.
* [ ] Validate each dataset.
* [ ] Add provenance.
* [ ] Add version identifiers.
* [ ] Make datasets accessible through the dataset catalog.

---

# 25. Testing

```text
tests/
├── unit/
├── connectors/
├── features/
└── integration/
```

### Tasks

* [ ] Acquisition tests.
* [ ] Parsing tests.
* [ ] Normalization tests.
* [ ] Validation tests.
* [ ] Metadata tests.
* [ ] Entity tests.
* [ ] Schema tests.
* [ ] Storage tests.
* [ ] Query tests.
* [ ] Export tests.
* [ ] Versioning tests.
* [ ] Migration tests.
* [ ] Connector tests.
* [ ] Feature tests.
* [ ] Integration tests.
* [ ] End-to-end tests.
* [ ] Regression tests.
* [ ] Failure/recovery tests.
* [ ] Schema compatibility tests.

---

# 26. Documentation

### Architecture

* [ ] Architecture overview.
* [ ] Connector architecture.
* [ ] Schema architecture.
* [ ] Parsing architecture.
* [ ] Normalization architecture.
* [ ] Validation architecture.
* [ ] Metadata architecture.
* [ ] Provenance architecture.
* [ ] Storage architecture.
* [ ] Query architecture.
* [ ] Entity architecture.
* [ ] Versioning architecture.

### Connectors

* [ ] Binance.
* [ ] Finnhub.
* [ ] FRED.
* [ ] GDELT.
* [ ] IMF.
* [ ] OpenSanctions.
* [ ] SEC.
* [ ] World Bank.
* [ ] YFinance.

### Developer documentation

* [ ] Connector development guide.
* [ ] Schema development guide.
* [ ] Normalizer development guide.
* [ ] Parser development guide.
* [ ] Validation development guide.
* [ ] Testing guide.
* [ ] Contribution guide.

---

# 27. Production Hardening

* [ ] Structured logging.
* [ ] Standardized error taxonomy.
* [ ] Retry policies.
* [ ] Rate-limit handling.
* [ ] Request timeouts.
* [ ] Memory limits.
* [ ] Streaming ingestion.
* [ ] Large-file handling.
* [ ] Checkpointing.
* [ ] Resumable ingestion.
* [ ] Atomic dataset writes.
* [ ] Dataset corruption detection.
* [ ] Deterministic pipelines.
* [ ] Reproducibility checks.
* [ ] Performance benchmarks.
* [ ] Memory benchmarks.
* [ ] Connector reliability tests.

---

# 28. Final Hermes v1 Acceptance Criteria

### Acquisition

* [ ] Reliable connector framework.
* [ ] Raw data acquisition.
* [ ] Cache.
* [ ] Retry.
* [ ] Pagination.
* [ ] Rate limiting.
* [ ] Incremental synchronization.

### Understanding

* [ ] Metadata extraction.
* [ ] Dataset inspection.
* [ ] Dataset profiling.

### Transformation

* [ ] Parsing.
* [ ] Canonical normalization.
* [ ] Explicit transformations.

### Trust

* [ ] Schema validation.
* [ ] Data-quality validation.
* [ ] Completeness checks.
* [ ] Freshness checks.
* [ ] Integrity checks.

### Identity

* [ ] Country resolution.
* [ ] Company resolution.
* [ ] General entity resolution.
* [ ] Canonical entity registry.

### Data management

* [ ] Dataset catalog.
* [ ] Dataset registry.
* [ ] Storage.
* [ ] Querying.
* [ ] Materialization.
* [ ] Export.

### Reproducibility

* [ ] Metadata.
* [ ] Provenance.
* [ ] Lineage.
* [ ] Dataset versioning.
* [ ] Snapshots.
* [ ] Dataset diff.
* [ ] Schema versioning.
* [ ] Schema migration.

### Developer experience

* [ ] Stable `hr.*` API.
* [ ] Stable connector contract.
* [ ] Documented canonical schemas.
* [ ] Reference connector.
* [ ] Complete test suite.
* [ ] Architecture documentation.
* [ ] Connector development documentation.

### Core success test

```text
CSV / JSON / API / XML
        ↓
      Hermes
        ↓
Parse → Normalize → Validate
        ↓
Metadata + Provenance + Lineage
        ↓
Canonical Dataset
        ↓
Store → Query → Version → Export
```

**The first milestone should not be "implement everything." The first real milestone is:**

```text
ONE SOURCE
    ↓
raw
    ↓
parse
    ↓
normalize
    ↓
canonical schema
    ↓
validate
    ↓
metadata
    ↓
provenance
    ↓
stored Dataset
```

Once that works cleanly end-to-end for one connector, the rest of Hermes becomes **repeating and generalizing the architecture**, rather than inventing the architecture separately for every source.
