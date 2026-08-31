from hermes.storage.base import StorageBackend


class DuckDBStorage(StorageBackend):

    def __init__(self, database_path: str = "~/.hermes/data/hermes.duckdb") -> None:
        self.database_path = database_path

    def save(self, dataset: object, path: str) -> None:
        ...

    def load(self, path: str) -> object:
        ...

    def delete(self, path: str) -> None:
        ...

    def exists(self, path: str) -> bool:
        ...

    def list(self, prefix: str = "") -> list[str]:
        ...

    def query(self, sql: str) -> object:
        ...
