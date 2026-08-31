from hermes.datasets.models import DatasetDescriptor


class DatasetRegistry:

    def __init__(self) -> None:
        self._datasets: dict[str, DatasetDescriptor] = {}

    def register(self, dataset: DatasetDescriptor) -> None:
        ...

    def get(self, dataset_id: str) -> DatasetDescriptor | None:
        ...

    def list(self) -> list[DatasetDescriptor]:
        ...

    def search(self, query: str) -> list[DatasetDescriptor]:
        ...
