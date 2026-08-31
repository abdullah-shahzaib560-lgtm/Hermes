from hermes.storage.base import StorageBackend


class ParquetStorage(StorageBackend):

    def __init__(self, base_path: str = "~/.hermes/data") -> None:
        self.base_path = base_path

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
