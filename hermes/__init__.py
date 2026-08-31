from hermes.api.acquire import fetch, ingest, read, sync
from hermes.api.data import parse, normalize, validate, transform, profile, inspect
from hermes.api.datasets import list_datasets, get_dataset, search_datasets
from hermes.api.entities import resolve_entity, resolve_country, resolve_company
from hermes.api.schemas import get_schema, register_schema, compare_schema, migrate
from hermes.api.storage import save, load, query, materialize
from hermes.core.dataset import Dataset
from hermes.core.config import configure, get_config
from hermes.core.result import Result
from hermes.core.errors import (
    HermesError,
    AcquisitionError,
    ParseError,
    SchemaError,
    NormalizationError,
    ValidationError,
    StorageError,
    QueryError,
    ConfigError,
    ConnectorNotFoundError,
    AuthenticationError,
)

__all__ = [
    # Fetching
    "fetch",
    "ingest",
    "read",
    "sync",
    # Data operations
    "parse",
    "normalize",
    "validate",
    "transform",
    "profile",
    "inspect",
    # Datasets
    "Dataset",
    "list_datasets",
    "get_dataset",
    "search_datasets",
    # Entities
    "resolve_entity",
    "resolve_country",
    "resolve_company",
    # Schemas
    "get_schema",
    "register_schema",
    "compare_schema",
    "migrate",
    # Storage
    "save",
    "load",
    "query",
    "materialize",
    # Config
    "configure",
    "get_config",
    # Core
    "Result",
    "HermesError",
    "AcquisitionError",
    "ParseError",
    "SchemaError",
    "NormalizationError",
    "ValidationError",
    "StorageError",
    "QueryError",
    "ConfigError",
    "ConnectorNotFoundError",
    "AuthenticationError",
]
