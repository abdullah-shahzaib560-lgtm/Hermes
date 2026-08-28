# Hermes Team Engineering Guide

## 1. Purpose

Hermes is being developed as a serious data platform, not just a collection of API connectors.

The team must be able to work independently without everyone needing to understand the entire codebase.

The core pipeline is:

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

Every contributor should understand where their work fits into this pipeline.

---

# 2. Team Roles

## Lead / Architect (Haider Ali)

Responsible for:

* Architecture
* Core abstractions
* Canonical schemas
* Connector contract
* Public API
* Entity resolution architecture
* Provenance and lineage architecture
* Storage architecture
* Difficult connectors
* Final architectural review
* Integration

The lead defines interfaces and rules so other engineers can implement components independently.

---

## Data Engineer (Abdul Rehman)

Responsible for:

* Acquisition
* Connectors
* Parsing
* Source-specific normalization
* Source mappings
* Connector tests

The data engineer turns external sources into Hermes-compatible datasets.

---

## Junior Engineer (Ibrahim)

Initially responsible for:

* Metadata
* Profiling
* Validation checks
* Unit tests
* Documentation
* Simple utilities
* Simple connectors after learning the system

The junior engineer should receive small, well-defined tasks and gradually take ownership of larger components.

---

# 3. Repository Ownership

```text
hermes/
├── api/                 → Lead
├── acquisition/         → Data Engineer
├── connectors/          → Data Engineer
├── core/                → Lead
├── schemas/             → Lead
├── parsing/             → Data Engineer
├── normalization/       → Data Engineer
├── validation/          → Junior Engineer
├── metadata/            → Junior Engineer
├── entities/            → Lead
├── datasets/            → Lead
├── storage/             → Lead
├── query/               → Lead
├── export/              → Junior Engineer
└── features/            → Shared
```

Ownership does not mean nobody else can modify a directory.

It means one person is responsible for understanding, maintaining, testing, and improving that subsystem.

---

# 4. Hermes Data Pipeline

## Acquisition

Acquisition gets data from the external source.

Responsibilities:

* HTTP/API requests
* Authentication
* Pagination
* Rate limits
* Retries
* Caching
* Synchronization
* Raw response handling

Acquisition should not decide what a source's fields mean.

---

## Raw Data

Raw data is the original source representation.

Examples:

```text
SEC JSON
World Bank JSON
GDELT CSV
FRED API response
Binance API response
```

Raw data should be preserved whenever practical.

Raw data is useful for:

* Reprocessing
* Debugging
* Auditing
* Reproducibility
* Detecting changes in source data

---

## Parsing

Parsing converts the source representation into structured records.

Example:

```text
Nested SEC JSON
        ↓
List of records
```

Parsing answers:

> How do I extract records from this source format?

Parsing does not answer:

> What should this field mean in Hermes?

That is normalization.

---

## Normalization

Normalization converts source-specific representations into Hermes representations.

Example:

```text
SEC:
us-gaap:Revenues

        ↓

Hermes:
revenue
```

Another example:

```text
World Bank:
Country Name

        ↓

Hermes:
entity_id
```

Normalization includes:

* Field mappings
* Type conversion
* Date normalization
* Timestamp normalization
* Country normalization
* Entity identifier normalization
* Unit normalization
* Currency normalization
* Missing-value conventions
* Source-specific semantic mappings

There is no universal magic normalizer that understands every dataset.

Hermes provides a common normalization engine, while each connector provides source-specific mappings and rules.

---

# 5. Canonical Schemas

A canonical schema defines how Hermes represents a particular class of data.

It is the contract between connectors and the rest of Hermes.

Example:

```text
External Source A
        ↓
      Mapping
        ↓
Canonical Hermes Schema
        ↑
      Mapping
        ↑
External Source B
```

This allows downstream users to work with a stable structure instead of learning every source's format.

Canonical schemas define:

* Field names
* Types
* Required fields
* Optional fields
* Units
* Identifiers
* Temporal meaning
* Constraints
* Schema version

Do not create one giant universal schema containing every possible field.

Create domain-specific canonical schemas.

---

# 6. Validation

Validation determines whether data satisfies Hermes expectations.

Examples:

```text
Is the timestamp valid?
Is the required entity ID present?
Is revenue numeric?
Are country codes valid?
Are duplicate primary keys present?
Are values inside allowed ranges?
Does the schema match?
```

Validation should produce a report.

Validation errors should be distinguishable from warnings.

---

# 7. Metadata

Metadata describes the dataset.

Example:

```text
rows
columns
column names
data types
null counts
unique counts
date range
frequency
duplicate count
source
retrieval time
schema
version
quality information
```

Metadata does not modify the dataset.

`hr.get_metadata(data)` should inspect the data and return information about it.

---

# 8. Provenance

Provenance answers:

> Where did this data come from?

Track:

* Source
* URL/API endpoint
* Retrieval timestamp
* Connector
* Connector version
* Raw-data checksum
* Parser version
* Normalizer version
* Schema version

---

# 9. Lineage

Lineage answers:

> What happened to this data?

Example:

```text
World Bank API
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

Every major transformation should be traceable.

---

# 10. Connector Rules

A connector is responsible for understanding one external source.

A connector should:

1. Acquire source data.
2. Preserve raw data.
3. Parse source-specific formats.
4. Map source fields to Hermes concepts.
5. Normalize values.
6. Declare the canonical schema.
7. Validate the resulting dataset.
8. Provide metadata and provenance.

A connector should NOT:

* Implement unrelated business logic.
* Contain generic validation logic.
* Contain generic HTTP retry logic.
* Implement generic caching.
* Modify unrelated datasets.
* Put feature engineering inside acquisition code.

Generic behavior belongs in Hermes infrastructure.

Source-specific behavior belongs in the connector.

---

# 11. Task Rules

Every engineering task must have:

* Task ID
* Title
* Owner
* Goal
* Background
* Input
* Expected output
* Files/subsystem
* Requirements
* Edge cases
* Tests
* Definition of done

Example:

```text
META-001

Title:
Implement column metadata extraction

Owner:
Junior Engineer

Goal:
Extract metadata for every dataset column.

Input:
Polars DataFrame

Output:
ColumnMetadata objects

Required:
- name
- dtype
- null_count
- null_ratio
- unique_count

Edge cases:
- Empty dataset
- Null-only column
- Duplicate values
- Mixed types

Tests:
- Normal dataset
- Empty dataset
- Null values
- Duplicate values

Done when:
- Implementation complete
- Tests pass
- Documentation updated
- Pull request opened
- Review completed
```

Never assign:

```text
Build metadata.
```

Assign:

```text
Implement META-001.
```

---

# 12. Difficulty Levels

## Beginner

Tasks involving:

* Small functions
* Tests
* Documentation
* Simple metadata
* Simple validation
* Small utilities

## Easy

Tasks involving:

* Small modules
* Simple connector components
* Basic parsing
* Basic mappings

## Medium

Tasks involving:

* Complete connectors
* Complex validation
* Storage functionality
* Query functionality

## Hard

Tasks involving:

* SEC normalization
* GDELT normalization
* Entity resolution
* Schema migrations
* Lineage
* Versioning
* Performance work

## Architecture

Architecture tasks should only be assigned after the engineer understands the subsystem.

---

# 13. Git Workflow

Never work directly on `main`.

Use:

```text
Issue
  ↓
Branch
  ↓
Implementation
  ↓
Tests
  ↓
Pull Request
  ↓
Review
  ↓
Merge
```

Branch examples:

```text
feature/meta-column-profile
feature/worldbank-normalizer
feature/fred-parser
fix/validation-null-check
test/sec-normalizer
docs/connector-guide
```

---

# 14. Pull Request Rules

Every PR should contain:

* What changed
* Why it changed
* Files affected
* Tests added
* Tests run
* Known limitations

Before opening a PR:

```text
[ ] Code works
[ ] Tests added
[ ] Existing tests pass
[ ] No unrelated changes
[ ] Type hints added where appropriate
[ ] Documentation updated if API changed
[ ] No secrets committed
```

---

# 15. Review Rules

The author is responsible for correctness.

The reviewer checks:

* Correctness
* Tests
* Architecture
* Maintainability
* Naming
* Error handling
* API compatibility
* Performance where relevant

The lead reviews:

* Architecture changes
* Public API changes
* Canonical schemas
* Cross-subsystem changes
* Entity resolution
* Storage architecture
* Major normalization decisions

---

# 16. Coding Rules

Prefer:

```text
Small functions
Clear names
Type hints
Explicit behavior
Tests
Documentation
Deterministic transformations
```

Avoid:

```text
Huge functions
Hidden global state
Magic behavior
Duplicated infrastructure
Source-specific logic in core
Untested transformations
Unnecessary abstractions
```

---

# 17. Important Architectural Rule

Do not solve the same infrastructure problem separately inside every connector.

Bad:

```text
World Bank → Own retry system
FRED       → Own retry system
IMF        → Own retry system
SEC        → Own retry system
```

Good:

```text
                 Hermes Acquisition
                 ├── Retry
                 ├── Cache
                 ├── Pagination
                 └── Rate Limiting
                         ↓
World Bank ──────────────┤
FRED ────────────────────┤
IMF ─────────────────────┤
SEC ─────────────────────┘
```

The connector provides source-specific behavior.

Hermes provides reusable infrastructure.

---

# 18. Learning While Building

New engineers should learn by implementing real Hermes tasks.

Do not give a beginner months of tutorials before allowing them to contribute.

Progression:

```text
Python basics
    ↓
Git
    ↓
pytest
    ↓
Polars
    ↓
Metadata
    ↓
Profiling
    ↓
Validation
    ↓
Simple parser
    ↓
Simple connector
    ↓
Normalization
    ↓
Complete connector
```

Every step should produce a real PR.

---

# 19. Communication Rules

When blocked, do not immediately ask:

> How do I build this?

First provide:

```text
What I am trying to do:
What I expected:
What actually happened:
What I tried:
Relevant error:
Relevant files:
```

Example:

```text
I am implementing META-003.

Expected:
Frequency detection should return monthly.

Actual:
It returns irregular.

I tested:
Dataset A and Dataset B.

Relevant:
hermes/metadata/extractor.py
```

This makes technical discussion much faster.

---

# 20. Current Team Assignment

## Lead

Priority:

```text
1. Core abstractions
2. Canonical schemas
3. BaseConnector
4. Reference connector architecture
5. Public API
6. Provenance/lineage design
7. Entity system design
```

## Data Engineer

Priority:

```text
1. Acquisition refactor
2. World Bank connector
3. FRED connector
4. IMF connector
5. YFinance connector
6. Finnhub connector
7. Binance connector
8. GDELT connector
9. SEC connector
```

## Junior Engineer

Priority:

```text
1. Git/PR workflow
2. Metadata extraction
3. Dataset profiling
4. Completeness checks
5. Quality checks
6. Freshness checks
7. Validation reports
8. Unit tests
9. Documentation
10. Simple connector
```

---

# 21. Definition of a Complete Connector

A connector is not complete just because the API request works.

A complete connector has:

```text
[ ] Acquisition
[ ] Raw data handling
[ ] Parsing
[ ] Source → Hermes mappings
[ ] Normalization
[ ] Canonical schema
[ ] Validation
[ ] Metadata
[ ] Provenance
[ ] Tests
[ ] Documentation
```

---

# 22. Definition of Done

A component is complete when:

```text
[ ] Design is understood
[ ] Implementation exists
[ ] Interface is defined
[ ] Tests exist
[ ] Edge cases are handled
[ ] Errors are handled
[ ] Documentation exists
[ ] Metadata/provenance implications are considered
[ ] Code has been reviewed
[ ] CI passes
```

---

# 23. Hermes Public API Goal

The team should ultimately make this possible:

```python
data = hr.fetch("world_bank", ...)

data = hr.normalize(data)

hr.validate(data)

hr.get_metadata(data)

hr.save(data)
```

The user should not need to understand:

* API pagination
* Source-specific field names
* Source-specific country codes
* Source-specific units
* Source-specific JSON structure
* Retry mechanics
* Cache implementation

Hermes handles those details.

---

# 24. Long-Term Engineering Goal

The team should be able to add a new source without redesigning Hermes.

```text
New Source
    ↓
New Connector
    ↓
Source Parser
    ↓
Source Mappings
    ↓
Canonical Schema
    ↓
Normalization
    ↓
Validation
    ↓
Metadata
    ↓
Provenance
```

If adding a new source requires modifying unrelated parts of Hermes, the architecture should be reviewed.

---

# 25. Team Development Philosophy

The objective is not simply to make the current three people productive.

The objective is to build an engineering system where new people can join later and become productive quickly.

Therefore:

```text
Architecture
      ↓
Interfaces
      ↓
Documentation
      ↓
Small Tasks
      ↓
Implementation
      ↓
Tests
      ↓
Review
      ↓
Integration
```

The system should reduce dependence on tribal knowledge.

---

# 26. Engineering Standard

Every contributor should eventually be able to answer:

```text
What does this subsystem do?

Why does it exist?

What does it accept?

What does it return?

What invariants must it maintain?

Where does source-specific logic belong?

Where does generic logic belong?

How is it tested?

How is it versioned?

How is its output traced back to the source?
```

If an engineer cannot answer these questions for their subsystem, they do not own it yet.

---

# 27. Immediate Team Goal

Do not attempt to build every Hermes subsystem simultaneously.

First make one complete vertical slice:

```text
World Bank
    ↓
_acquire()
    ↓
raw data
    ↓
parse()
    ↓
normalize()
    ↓
canonical schema
    ↓
validate()
    ↓
metadata
    ↓
provenance
    ↓
Dataset
```

Once this works cleanly, use it as the reference implementation for the rest of Hermes.

The architecture should be proven by working code before expanding it.

"""
