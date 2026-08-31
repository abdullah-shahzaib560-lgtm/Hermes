# Hermes Core

## Internal Engineering Checklist

**Purpose:** Build Hermes Core as a general-purpose data lifecycle engine. Connectors and domain-specific packages must remain separate from Core.

---

## 1. Core Architecture

### Fundamental lifecycle

* [ ] Define the Hermes data lifecycle
* [ ] Define the internal representation shared by all ingestion paths
* [ ] Ensure API sources and file sources converge into the same internal representation
* [ ] Define Dataset as the central abstraction
* [ ] Define clear boundaries between Core and domain packages
* [ ] Define extension interfaces for connectors, parsers, schemas, validators, transforms, resolvers and storage

### Core subsystems

* [ ] Acquisition
* [ ] Parsing
* [ ] Data Contract
* [ ] Quality
* [ ] Transformation
* [ ] Identity
* [ ] Dataset
* [ ] Execution & Storage

---

# 2. Dataset Abstraction

### Dataset object

* [ ] Define `Dataset`
* [ ] Dataset contains data representation
* [ ] Dataset contains schema information
* [ ] Dataset contains metadata
* [ ] Dataset contains provenance
* [ ] Dataset contains lineage
* [ ] Dataset contains version information
* [ ] Dataset supports lazy/eager execution where appropriate
* [ ] Dataset methods return consistent Dataset/results
* [ ] Dataset integrates with Arrow
* [ ] Dataset integrates with Polars
* [ ] Dataset integrates with Pandas
* [ ] Dataset integrates with DuckDB

### Dataset operations

* [ ] `dataset.parse()`
* [ ] `dataset.normalize()`
* [ ] `dataset.validate()`
* [ ] `dataset.profile()`
* [ ] `dataset.inspect()`
* [ ] `dataset.transform()`
* [ ] `dataset.resolve()`
* [ ] `dataset.query()`
* [ ] `dataset.save()`
* [ ] `dataset.export()`
* [ ] `dataset.metadata()`
* [ ] `dataset.schema()`
* [ ] `dataset.lineage()`

---

# 3. Acquisition Engine

### Source abstraction

* [ ] Define `Source`
* [ ] Define source configuration
* [ ] Define source credentials/configuration handling
* [ ] Define source capabilities
* [ ] Define source metadata
* [ ] Define source lifecycle

### Acquisition API

* [ ] Implement `fetch()`
* [ ] Implement `ingest()`
* [ ] Implement `source()`
* [ ] Implement `connect()`
* [ ] Implement `read()`
* [ ] Implement `stream()`

### Requirements

* [ ] API sources supported
* [ ] File sources supported
* [ ] Local sources supported
* [ ] Streaming sources have a defined interface
* [ ] Acquisition failures produce structured errors
* [ ] Source information is recorded in provenance

---

# 4. Parsing Engine

### Parser abstraction

* [ ] Define `Parser`
* [ ] Define parser interface
* [ ] Define parser input contract
* [ ] Define parser output contract
* [ ] Define parser registration system
* [ ] Define parser selection mechanism

### Parsing operations

* [ ] Implement `parse()`
* [ ] Implement `detect_format()`
* [ ] Implement `read_raw()`
* [ ] Implement `decode()`

### Initial formats

* [ ] CSV
* [ ] JSON
* [ ] JSONL
* [ ] XML
* [ ] Parquet
* [ ] Arrow
* [ ] Compressed files

### Separation requirements

* [ ] Parser does not perform semantic normalization
* [ ] Parser does not perform entity resolution
* [ ] Parser does not contain domain-specific mappings
* [ ] Parser preserves source information where required

---

# 5. Data Contract / Schema Engine

### Schema abstraction

* [ ] Define Hermes schema model
* [ ] Define field model
* [ ] Define data type model
* [ ] Define nullable fields
* [ ] Define required fields
* [ ] Define constraints
* [ ] Define schema versioning
* [ ] Define schema serialization

### Schema operations

* [ ] Implement `schema()`
* [ ] Implement `register_schema()`
* [ ] Implement `infer_schema()`
* [ ] Implement `validate_schema()`
* [ ] Implement `compare_schema()`
* [ ] Implement `migrate_schema()`
* [ ] Implement `metadata()`
* [ ] Implement `set_metadata()`

### Schema requirements

* [ ] Source schemas supported
* [ ] Canonical Hermes schemas supported
* [ ] Schema compatibility checking
* [ ] Schema evolution
* [ ] Schema version tracking
* [ ] Schema migration support
* [ ] Schema registration

---

# 6. Normalization Engine

### Normalization model

* [ ] Define normalization interface
* [ ] Define source-to-canonical mapping
* [ ] Define canonical field representation
* [ ] Define type normalization
* [ ] Define unit normalization
* [ ] Define temporal normalization
* [ ] Define geographic normalization
* [ ] Define identifier normalization

### Operations

* [ ] Implement `normalize()`
* [ ] Implement `map()`
* [ ] Implement `cast()`
* [ ] Implement `standardize()`
* [ ] Implement `convert_units()`
* [ ] Implement `align_time()`
* [ ] Implement `clean()`

### Requirements

* [ ] ISO date/time conventions
* [ ] Consistent timezone handling
* [ ] Standard country codes
* [ ] Consistent numeric types
* [ ] Unit conversion framework
* [ ] Source-specific mappings remain outside generic Core
* [ ] Normalization is deterministic
* [ ] Normalization steps are recorded in lineage

---

# 7. Quality Engine

### Quality framework

* [ ] Define quality check interface
* [ ] Define validation rule interface
* [ ] Define quality report
* [ ] Define quality score/reporting model
* [ ] Define severity levels
* [ ] Define warning vs error behavior

### Validation

* [ ] Implement `validate()`
* [ ] Implement `check()`
* [ ] Null checks
* [ ] Type checks
* [ ] Range checks
* [ ] Required-field checks
* [ ] Constraint checks
* [ ] Referential checks where applicable

### Profiling

* [ ] Implement `profile()`
* [ ] Row count
* [ ] Column count
* [ ] Data types
* [ ] Null percentage
* [ ] Unique values
* [ ] Duplicate counts
* [ ] Min/max
* [ ] Basic statistics
* [ ] Distribution information
* [ ] Temporal coverage
* [ ] Frequency detection
* [ ] Gap detection

### Deduplication

* [ ] Implement `deduplicate()`
* [ ] Exact duplicate detection
* [ ] Configurable duplicate keys
* [ ] Duplicate resolution strategy
* [ ] Preserve duplicate information when required

### Anomaly detection

* [ ] Implement `detect_anomalies()`
* [ ] Define anomaly interface
* [ ] Keep advanced anomaly models extensible
* [ ] Do not couple Core to ML-specific implementations

### Quality reporting

* [ ] Implement `quality()`
* [ ] Produce machine-readable report
* [ ] Produce human-readable report
* [ ] Record quality results in metadata/provenance

---

# 8. Transformation Engine

### Transformation abstraction

* [ ] Define `Transformer`
* [ ] Define transformation input/output contract
* [ ] Define transformation composition
* [ ] Define transformation registration
* [ ] Define transformation execution

### Operations

* [ ] Implement `transform()`
* [ ] Implement `pipe()`
* [ ] Implement `apply()`
* [ ] Implement `select()`
* [ ] Implement `filter()`
* [ ] Implement `join()`
* [ ] Implement `aggregate()`

### Requirements

* [ ] Accept user-defined Python functions
* [ ] Support transformation pipelines
* [ ] Preserve schema information where possible
* [ ] Record transformations in lineage
* [ ] Avoid recreating Pandas functionality
* [ ] Use Polars/Arrow/DuckDB where appropriate

---

# 9. Identity / Entity Resolution Interface

### Resolver abstraction

* [ ] Define `Resolver`
* [ ] Define resolver interface
* [ ] Define resolver registration
* [ ] Define resolver configuration
* [ ] Define match result model
* [ ] Define canonical entity representation

### Operations

* [ ] Implement `resolve()`
* [ ] Implement `identify()`
* [ ] Implement `match()`
* [ ] Implement `link()`
* [ ] Implement `entity()`

### Architecture requirements

* [ ] Core provides the resolver interface
* [ ] Domain-specific entity knowledge remains outside Core
* [ ] Corporate resolver can be added independently
* [ ] Financial identifiers can be added independently
* [ ] Defense identifiers can be added independently
* [ ] Healthcare identifiers can be added independently

---

# 10. Storage Engine

### Storage abstraction

* [ ] Define `StorageBackend`
* [ ] Define storage interface
* [ ] Define dataset persistence format
* [ ] Define dataset location model
* [ ] Define storage metadata
* [ ] Define storage lifecycle

### Operations

* [ ] Implement `save()`
* [ ] Implement `load()`
* [ ] Implement `delete()`
* [ ] Implement dataset existence checks

### Initial storage targets

* [ ] Local filesystem
* [ ] Parquet
* [ ] Arrow
* [ ] DuckDB
* [ ] PostgreSQL where appropriate

### Requirements

* [ ] Storage backend is pluggable
* [ ] Dataset metadata persists with dataset
* [ ] Schema persists with dataset
* [ ] Version information persists with dataset
* [ ] Provenance persists with dataset

---

# 11. Query Engine

### Query abstraction

* [ ] Define query interface
* [ ] Define query execution model
* [ ] Define query result abstraction

### Operations

* [ ] Implement `query()`
* [ ] Implement `sql()`
* [ ] Support filtering
* [ ] Support projections
* [ ] Support joins
* [ ] Support aggregations
* [ ] Support ordering
* [ ] Support limits

### Integrations

* [ ] DuckDB integration
* [ ] Polars integration
* [ ] Arrow integration
* [ ] Pandas integration

---

# 12. Export Engine

### Export abstraction

* [ ] Define exporter interface
* [ ] Define export configuration
* [ ] Define export metadata

### Operations

* [ ] Implement `export()`
* [ ] Implement `to_arrow()`
* [ ] Implement `to_polars()`
* [ ] Implement `to_pandas()`
* [ ] Implement `to_duckdb()`

### Initial formats

* [ ] Parquet
* [ ] CSV
* [ ] JSON
* [ ] JSONL
* [ ] Arrow

---

# 13. Dataset Versioning

### Version model

* [ ] Define dataset version
* [ ] Define schema version
* [ ] Define pipeline version
* [ ] Define version identifiers
* [ ] Define version metadata

### Operations

* [ ] Implement `version()`
* [ ] Implement `snapshot()`
* [ ] Implement `diff()`

### Requirements

* [ ] Immutable snapshots
* [ ] Snapshot metadata
* [ ] Snapshot provenance
* [ ] Snapshot lineage
* [ ] Schema associated with every version
* [ ] Ability to compare dataset versions
* [ ] Ability to identify changes between versions

---

# 14. Provenance & Lineage

### Provenance

* [ ] Define provenance model
* [ ] Record original source
* [ ] Record source version where available
* [ ] Record acquisition time
* [ ] Record parser version
* [ ] Record normalization version
* [ ] Record validation results
* [ ] Record resolver information
* [ ] Record dataset version

### Lineage

* [ ] Define lineage model
* [ ] Record ordered transformation steps
* [ ] Record component versions
* [ ] Record inputs/outputs
* [ ] Implement `lineage()`
* [ ] Implement `provenance()`
* [ ] Implement `trace()`

### Initial implementation

* [ ] Start with ordered lineage records
* [ ] Do not build a DAG initially
* [ ] Design the model so a DAG can be added later

---

# 15. Registry System

### Registry abstractions

* [ ] Define component registry
* [ ] Define dataset registry
* [ ] Define schema registry
* [ ] Define connector registry
* [ ] Define parser registry
* [ ] Define validator registry
* [ ] Define transformer registry
* [ ] Define resolver registry
* [ ] Define storage registry

### Operations

* [ ] Implement `register()`
* [ ] Implement component lookup
* [ ] Implement component discovery
* [ ] Implement component versioning
* [ ] Implement component metadata

---

# 16. Execution Engine

### Pipeline execution

* [ ] Define execution context
* [ ] Define pipeline abstraction
* [ ] Define execution state
* [ ] Define execution results
* [ ] Define error handling
* [ ] Define retry behavior where applicable

### Requirements

* [ ] Execute pipeline stages in deterministic order
* [ ] Pass Dataset between stages
* [ ] Capture lineage automatically
* [ ] Capture execution metadata
* [ ] Capture errors
* [ ] Support reusable pipelines
* [ ] Support configurable execution

---

# 17. Inspection / Developer Experience

### Inspection

* [ ] Implement `inspect()`
* [ ] Display dataset dimensions
* [ ] Display schema
* [ ] Display metadata
* [ ] Display sample records
* [ ] Display quality information
* [ ] Display lineage
* [ ] Display provenance
* [ ] Display version information

### CLI/TUI

* [ ] Dataset inspection command
* [ ] Schema inspection command
* [ ] Profile command
* [ ] Validation command
* [ ] Lineage command
* [ ] Dataset catalog command

---

# 18. Error System

* [ ] Define Hermes exception hierarchy
* [ ] Define acquisition errors
* [ ] Define parsing errors
* [ ] Define schema errors
* [ ] Define normalization errors
* [ ] Define validation errors
* [ ] Define transformation errors
* [ ] Define resolution errors
* [ ] Define storage errors
* [ ] Define query errors
* [ ] Define configuration errors
* [ ] Provide useful error context
* [ ] Preserve original source errors where appropriate

---

# 19. Extension Architecture

### Connector plugin

* [ ] Define connector interface
* [ ] Define connector configuration
* [ ] Define connector metadata
* [ ] Define connector lifecycle
* [ ] Ensure connectors depend on Core, not vice versa

### Plugin interfaces

* [ ] Connector
* [ ] Parser
* [ ] Schema
* [ ] Mapper
* [ ] Normalizer
* [ ] Validator
* [ ] Profiler
* [ ] Transformer
* [ ] Resolver
* [ ] Storage backend
* [ ] Exporter

### Dependency rule

* [ ] Core must not depend on Finance
* [ ] Core must not depend on Defense
* [ ] Core must not depend on Healthcare
* [ ] Core must not contain domain-specific semantics
* [ ] Domain packages may depend on Core

---

# 20. Python Ecosystem Integration

### Arrow

* [ ] Arrow-native internal interoperability
* [ ] Arrow conversion
* [ ] Arrow schema mapping

### Polars

* [ ] Dataset to Polars
* [ ] Polars input ingestion
* [ ] Polars transformations where appropriate

### Pandas

* [ ] Dataset to Pandas
* [ ] Pandas input ingestion

### DuckDB

* [ ] Dataset querying through DuckDB
* [ ] SQL execution
* [ ] Parquet querying

### NumPy

* [ ] Numeric interoperability where appropriate

---

# 21. Public API

### Initial API

* [ ] `hr.fetch()`
* [ ] `hr.ingest()`
* [ ] `hr.parse()`
* [ ] `hr.normalize()`
* [ ] `hr.validate()`
* [ ] `hr.profile()`
* [ ] `hr.inspect()`
* [ ] `hr.transform()`
* [ ] `hr.query()`
* [ ] `hr.save()`
* [ ] `hr.load()`
* [ ] `hr.export()`

### Dataset API

* [ ] `Dataset.parse()`
* [ ] `Dataset.normalize()`
* [ ] `Dataset.validate()`
* [ ] `Dataset.profile()`
* [ ] `Dataset.inspect()`
* [ ] `Dataset.transform()`
* [ ] `Dataset.resolve()`
* [ ] `Dataset.query()`
* [ ] `Dataset.save()`
* [ ] `Dataset.export()`
* [ ] `Dataset.schema()`
* [ ] `Dataset.metadata()`
* [ ] `Dataset.lineage()`

---

# 22. Testing

### Unit tests

* [ ] Acquisition
* [ ] Parsing
* [ ] Schema
* [ ] Normalization
* [ ] Validation
* [ ] Profiling
* [ ] Transformation
* [ ] Resolution
* [ ] Storage
* [ ] Query
* [ ] Export
* [ ] Versioning
* [ ] Provenance
* [ ] Lineage
* [ ] Registry

### Integration tests

* [ ] API → Parser → Dataset
* [ ] File → Parser → Dataset
* [ ] Dataset → Normalize → Validate
* [ ] Dataset → Profile → Quality report
* [ ] Dataset → Store → Load
* [ ] Dataset → Query → Export
* [ ] Dataset → Snapshot → Diff
* [ ] Full connector pipeline

### Contract tests

* [ ] Connector interface
* [ ] Parser interface
* [ ] Validator interface
* [ ] Transformer interface
* [ ] Resolver interface
* [ ] Storage interface

---

# 23. Initial Implementation Order

## Phase 1: Foundation

* [ ] `Dataset`
* [ ] Internal data representation
* [ ] Schema model
* [ ] Metadata model
* [ ] Error system
* [ ] Component interfaces

## Phase 2: Data In

* [ ] `ingest()`
* [ ] `fetch()`
* [ ] Parser system
* [ ] CSV parser
* [ ] JSON parser
* [ ] Parquet parser

## Phase 3: Data Contract

* [ ] Schema inference
* [ ] Schema registration
* [ ] Schema validation
* [ ] Metadata

## Phase 4: Data Quality

* [ ] Validation framework
* [ ] Profiling
* [ ] Deduplication
* [ ] Quality reports

## Phase 5: Normalization

* [ ] Mapping framework
* [ ] Type casting
* [ ] Date/time normalization
* [ ] Unit normalization
* [ ] Canonical schema mapping

## Phase 6: Transformation

* [ ] Transformation interface
* [ ] Pipeline composition
* [ ] User-defined transformations
* [ ] Polars/Arrow integration

## Phase 7: Storage & Query

* [ ] Storage interface
* [ ] Local/Parquet storage
* [ ] DuckDB integration
* [ ] Query engine
* [ ] Export system

## Phase 8: Dataset Lifecycle

* [ ] Dataset registry
* [ ] Snapshots
* [ ] Versioning
* [ ] Diff
* [ ] Provenance
* [ ] Lineage

## Phase 9: Identity

* [ ] Resolver interface
* [ ] Entity model
* [ ] Resolver registration
* [ ] First external resolver implementation

## Phase 10: Developer Experience

* [ ] `inspect()`
* [ ] CLI
* [ ] TUI
* [ ] Documentation
* [ ] Examples
* [ ] End-to-end workflows

---

# 24. Core Completion Criteria

Hermes Core should not be considered complete merely because all functions exist.

### A developer should be able to:

* [ ] Load a local CSV
* [ ] Load a JSON response
* [ ] Load a Parquet dataset
* [ ] Fetch data through a connector
* [ ] Automatically parse supported formats
* [ ] Inspect the inferred schema
* [ ] Define or select a canonical schema
* [ ] Normalize source data
* [ ] Validate the resulting dataset
* [ ] Profile the dataset
* [ ] Detect duplicates
* [ ] Apply custom transformations
* [ ] Query the dataset
* [ ] Convert it to Polars
* [ ] Convert it to Pandas
* [ ] Convert it to Arrow
* [ ] Query it through DuckDB
* [ ] Save it
* [ ] Load it later
* [ ] Create an immutable snapshot
* [ ] Compare two versions
* [ ] Inspect provenance
* [ ] Inspect lineage
* [ ] Export the final dataset

### Architectural requirements

* [ ] Core remains domain-agnostic
* [ ] Connectors are plugins
* [ ] Domain packages extend Core
* [ ] Dataset is the central abstraction
* [ ] Parsers do not perform semantic normalization
* [ ] Normalizers do not contain source acquisition logic
* [ ] Validators are independent components
* [ ] Entity resolution is an extension point
* [ ] Storage is pluggable
* [ ] Query execution is separated from storage
* [ ] Provenance is automatic
* [ ] Lineage is automatic
* [ ] Every major component is testable independently
* [ ] Hermes does not attempt to replace Pandas, Polars, Arrow or DuckDB
