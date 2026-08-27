# Hermes Data Platform — Internal Engineering Checklist

> **Goal:** Hermes must acquire external data, preserve the source truth, transform it into stable Hermes representations, validate it, track its provenance, and make it reliably available to downstream systems.

---

## 1. Connector Contract

Every connector should follow the same lifecycle.

* [ ] Implement `_fetch()`

  * [ ] Handle HTTP/API communication
  * [ ] Handle pagination
  * [ ] Handle retries
  * [ ] Handle rate limits
  * [ ] Return raw source data
  * [ ] Do **not** modify source data

* [ ] Implement `fetch()`

  * [ ] Public user-facing method
  * [ ] Handle caching
  * [ ] Call `_fetch()`
  * [ ] Parse raw response
  * [ ] Normalize parsed records
  * [ ] Validate normalized data
  * [ ] Return Hermes-compatible data

* [ ] Implement `fetch_raw()`

  * [ ] Return source data without normalization
  * [ ] Preserve original structure
  * [ ] Useful for debugging and provenance

---

# 2. Parsing

> Parsing converts a source-specific response into usable records. It does **not** attempt to make the data universal.

For every connector:

* [ ] Identify the raw response structure
* [ ] Extract individual records
* [ ] Flatten nested structures where necessary
* [ ] Preserve source-specific fields
* [ ] Preserve source identifiers
* [ ] Preserve source concepts/tags
* [ ] Handle malformed records safely
* [ ] Never silently discard unknown fields

Example:

```text
SEC JSON
    ↓
SEC records
```

Not:

```text
SEC JSON
    ↓
Universal Hermes data
```

---

# 3. Normalization

> Normalization converts source-specific records into Hermes canonical representations.

* [ ] Define the appropriate Hermes domain model
* [ ] Map source fields → canonical fields
* [ ] Normalize column/field names
* [ ] Normalize data types
* [ ] Normalize dates/timestamps
* [ ] Normalize missing values
* [ ] Normalize units where possible
* [ ] Normalize currencies where possible
* [ ] Normalize country identifiers
* [ ] Normalize entity identifiers
* [ ] Normalize categorical values where mappings exist
* [ ] Preserve original source values when useful
* [ ] Preserve `source`
* [ ] Preserve `source_id`
* [ ] Preserve `source_concept`
* [ ] Never guess semantic meaning when uncertain
* [ ] Never silently destroy source information

### Important

**Generic normalization engine ≠ generic source mapping.**

The engine is reusable.

The mappings are source/domain-specific.

```text
Generic engine
      +
SEC mappings
      ↓
SEC → Hermes
```

```text
Generic engine
      +
GDELT mappings
      ↓
GDELT → Hermes
```

---

# 4. Canonical Schemas

* [ ] Define stable Hermes domain models
* [ ] Keep schemas independent of external provider naming
* [ ] Avoid creating one universal schema for every dataset
* [ ] Separate domains where semantics differ

Initial canonical domains:

* [ ] Entity
* [ ] Document
* [ ] Financial Observation
* [ ] Economic Observation
* [ ] Market Observation
* [ ] Geopolitical Event
* [ ] Security Event
* [ ] Sanctioned Entity

For every canonical model:

* [ ] Define required fields
* [ ] Define optional fields
* [ ] Define data types
* [ ] Define units
* [ ] Define identifiers
* [ ] Define primary key
* [ ] Define semantic meaning
* [ ] Define allowed/null behavior
* [ ] Define source/provenance fields

---

# 5. Source → Hermes Mapping

Every complex connector should have explicit mappings.

* [ ] Identify source concepts
* [ ] Map source concepts → Hermes concepts
* [ ] Document ambiguous mappings
* [ ] Assign mapping confidence where appropriate
* [ ] Preserve original source concept
* [ ] Version mappings
* [ ] Test mappings against real source data

Example:

```text
SEC
us-gaap:Revenues
        ↓
Hermes
revenue
```

Never assume:

```text
"Revenue"
=
"Net Revenue"
=
"Sales"
```

unless the source semantics support it.

---

# 6. Validation

Every normalized dataset should be validated.

### Schema

* [ ] Required fields exist
* [ ] Unexpected fields handled
* [ ] Data types correct
* [ ] Schema version compatible

### Values

* [ ] Null checks
* [ ] Range checks
* [ ] Type checks
* [ ] Unit checks
* [ ] Currency checks
* [ ] Identifier checks

### Integrity

* [ ] Primary-key uniqueness
* [ ] Duplicate detection
* [ ] Referential integrity
* [ ] Temporal consistency
* [ ] Entity consistency

### Temporal

* [ ] Date parsing
* [ ] Date ordering
* [ ] Expected frequency
* [ ] Missing periods
* [ ] Future dates where invalid
* [ ] Timezone consistency

### Quality

* [ ] Missingness percentage
* [ ] Duplicate percentage
* [ ] Invalid-record percentage
* [ ] Coverage period
* [ ] Entity coverage

Validation must produce a **report**, not only `True/False`.

---

# 7. Metadata

Every dataset should have machine-readable metadata.

* [ ] Dataset name
* [ ] Dataset description
* [ ] Source
* [ ] Source URL
* [ ] Retrieval timestamp
* [ ] Coverage period
* [ ] Frequency
* [ ] Entity type
* [ ] Units
* [ ] Currency
* [ ] Schema version
* [ ] Connector version
* [ ] Row count
* [ ] Column count
* [ ] Data quality information
* [ ] Update frequency
* [ ] Last successful update

Public API:

```python
hr.get_metadata(data)
```

---

# 8. Dataset Profiling

Implement:

```python
hr.inspect(data)
hr.profile(data)
```

### `inspect()`

Quick overview:

* [ ] Shape
* [ ] Columns
* [ ] Types
* [ ] Missingness
* [ ] Date range
* [ ] Basic statistics

### `profile()`

Deep analysis:

* [ ] Distributions
* [ ] Quantiles
* [ ] Cardinality
* [ ] Missing-value patterns
* [ ] Outliers
* [ ] Temporal gaps
* [ ] Duplicate patterns
* [ ] Entity coverage

---

# 9. Data Quality

Implement:

```python
hr.check_quality(data)
hr.check_completeness(data)
hr.check_freshness(data)
hr.check_integrity(data)
hr.check_duplicates(data)
```

Every check should produce structured results.

Example:

```text
Dataset: world_bank.gdp

Quality: 96.4%

Errors:
    12 invalid country codes

Warnings:
    4.2% missing values
    2 missing annual observations

Freshness:
    3 days behind expected update
```

---

# 10. Provenance

Every dataset must answer:

> Where did this data come from?

Track:

* [ ] Source
* [ ] Source URL/API
* [ ] Request parameters
* [ ] Retrieval timestamp
* [ ] Raw response identifier/checksum
* [ ] Connector version
* [ ] Parser version
* [ ] Normalization version
* [ ] Schema version
* [ ] Validation result
* [ ] Dataset version

Implement:

```python
hr.get_provenance(data)
hr.get_lineage(data)
```

---

# 11. Dataset Lineage

Hermes should be able to explain:

```text
Source
  ↓
Raw
  ↓
Parsed
  ↓
Normalized
  ↓
Validated
  ↓
Stored
  ↓
Derived Dataset
```

* [ ] Track transformations
* [ ] Track transformation versions
* [ ] Track source datasets
* [ ] Track derived datasets
* [ ] Track dependencies
* [ ] Make lineage queryable

---

# 12. Versioning

Datasets must be reproducible.

Implement:

```python
hr.version(dataset)
hr.snapshot(dataset)
hr.diff(dataset_a, dataset_b)
```

* [ ] Dataset version
* [ ] Schema version
* [ ] Connector version
* [ ] Mapping version
* [ ] Normalization version
* [ ] Content checksum
* [ ] Immutable snapshots
* [ ] Dataset comparison

`diff()` should identify:

* [ ] Added records
* [ ] Removed records
* [ ] Changed records
* [ ] Schema changes
* [ ] Metadata changes

---

# 13. Schema Registry

Create a central schema registry.

* [ ] Register schemas
* [ ] Retrieve schemas
* [ ] Version schemas
* [ ] Compare schemas
* [ ] Validate compatibility
* [ ] Migrate between schema versions

API:

```python
hr.register_schema(...)
hr.get_schema(...)
hr.compare_schema(...)
hr.validate_schema(...)
hr.migrate(...)
```

---

# 14. Entity Resolution

Create canonical entities independent of source identifiers.

Implement:

```python
hr.resolve_country(...)
hr.resolve_company(...)
hr.resolve_entity(...)
hr.resolve_currency(...)
```

Support:

* [ ] ISO codes
* [ ] Source-specific IDs
* [ ] Company identifiers
* [ ] Country names
* [ ] Aliases
* [ ] External identifiers
* [ ] Entity relationships

Example:

```text
"United States"
"USA"
"US"
"840"
        ↓
Hermes Entity
        ↓
country_code = USA
```

---

# 15. Source Synchronization

Implement:

```python
hr.sync(...)
```

The goal:

* [ ] Detect existing data
* [ ] Detect new records
* [ ] Detect changed records
* [ ] Avoid unnecessary downloads
* [ ] Support incremental updates
* [ ] Support resumable ingestion
* [ ] Track last successful synchronization
* [ ] Handle source corrections/deletions

Especially important for:

* [ ] GDELT
* [ ] ACLED
* [ ] Market data
* [ ] SEC
* [ ] Other continuously updated sources

---

# 16. Dataset Registry

Hermes should know what datasets it has.

Implement:

```python
hr.datasets.list()
hr.datasets.get(...)
hr.datasets.search(...)
```

Each dataset should expose:

* [ ] Name
* [ ] Description
* [ ] Source
* [ ] Schema
* [ ] Version
* [ ] Coverage
* [ ] Frequency
* [ ] Last update
* [ ] Size
* [ ] Quality
* [ ] Availability

---

# 17. Storage

Hermes should separate **data representation** from **storage**.

Implement:

```python
hr.save(...)
hr.load(...)
hr.exists(...)
hr.delete(...)
```

Storage should support:

* [ ] Parquet
* [ ] Arrow
* [ ] DuckDB
* [ ] PostgreSQL where appropriate
* [ ] Partitioning
* [ ] Compression
* [ ] Dataset versioning

---

# 18. Query

Users shouldn't need to know how Hermes stores the data.

Implement:

```python
hr.query(...)
```

Support:

* [ ] Filtering
* [ ] Date ranges
* [ ] Entity filtering
* [ ] Column selection
* [ ] Aggregation
* [ ] Joins
* [ ] Version selection
* [ ] Lazy execution where possible

---

# 19. Materialization

Allow users to request the representation they need.

```python
hr.materialize(
    dataset="...",
    format="polars"
)
```

Support:

* [ ] Polars
* [ ] Pandas
* [ ] Arrow
* [ ] DuckDB
* [ ] JSON
* [ ] CSV
* [ ] Parquet

---

# 20. Data Contracts

Every important dataset should have a contract.

Contract should define:

* [ ] Schema
* [ ] Required fields
* [ ] Primary key
* [ ] Expected frequency
* [ ] Expected update interval
* [ ] Allowed null percentage
* [ ] Valid ranges
* [ ] Valid identifiers
* [ ] Unit expectations
* [ ] Freshness requirements

Detect:

```text
SOURCE CHANGE
        ↓
DATA CONTRACT FAILURE
        ↓
STOP / WARN
```

Never silently ingest a breaking source change.

---

# 21. Connector-Specific Requirements

### Every connector

* [ ] `_fetch()`
* [ ] `fetch()`
* [ ] `fetch_raw()`
* [ ] `parse()`
* [ ] `normalize()`
* [ ] `validate()`
* [ ] Metadata
* [ ] Provenance
* [ ] Tests
* [ ] Documentation

### Complex connectors

Also:

* [ ] Source mappings
* [ ] Canonical schema
* [ ] Entity resolution
* [ ] Incremental sync
* [ ] Source-specific validation
* [ ] Schema/version compatibility

---

# 22. Testing

Every connector must have:

* [ ] Unit tests
* [ ] Parsing tests
* [ ] Normalization tests
* [ ] Validation tests
* [ ] Malformed-data tests
* [ ] Empty-response tests
* [ ] API-error tests
* [ ] Pagination tests
* [ ] Cache tests
* [ ] Retry tests
* [ ] Schema regression tests
* [ ] Real-source fixture tests

Never rely only on live APIs for tests.

---

# 23. Core Public API Target

The long-term public API should feel approximately like:

```python
# Acquire
hr.fetch(...)
hr.fetch_raw(...)
hr.sync(...)

# Understand
hr.inspect(...)
hr.get_metadata(...)
hr.profile(...)

# Transform
hr.parse(...)
hr.normalize(...)
hr.transform(...)

# Verify
hr.validate(...)
hr.check_quality(...)
hr.check_completeness(...)
hr.check_freshness(...)
hr.check_integrity(...)

# Entities
hr.resolve_entity(...)
hr.resolve_country(...)
hr.resolve_company(...)

# Datasets
hr.datasets.list(...)
hr.datasets.get(...)
hr.datasets.search(...)

# Storage
hr.save(...)
hr.load(...)
hr.query(...)
hr.materialize(...)

# Provenance
hr.get_provenance(...)
hr.get_lineage(...)

# Versioning
hr.version(...)
hr.snapshot(...)
hr.diff(...)

# Schemas
hr.get_schema(...)
hr.register_schema(...)
hr.compare_schema(...)
hr.migrate(...)
```

---

# Hermes Core Principle

Every feature added to Hermes should answer at least one of these:

> **Can Hermes acquire data more reliably?**

> **Can Hermes understand data better?**

> **Can Hermes standardize data without destroying source information?**

> **Can Hermes prove where data came from?**

> **Can Hermes detect bad/broken data?**

> **Can Hermes reproduce a dataset?**

> **Can Hermes make heterogeneous sources interoperable?**

> **Can Hermes serve the data efficiently to downstream systems?**

