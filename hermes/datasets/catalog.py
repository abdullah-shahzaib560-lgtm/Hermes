from hermes.datasets.models import DatasetDescriptor
from hermes.datasets.registry import DatasetRegistry


class DatasetCatalog:

    def __init__(self) -> None:
        self._registry = DatasetRegistry()

    def list(self) -> list[DatasetDescriptor]:
        ...

    def get(self, dataset_id: str) -> DatasetDescriptor | None:
        ...

    def search(self, query: str) -> list[DatasetDescriptor]:
        ...

    def register(self, dataset: DatasetDescriptor) -> None:
        ...
