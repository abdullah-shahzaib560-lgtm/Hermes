from hermes.core.result import Result


def list_datasets() -> Result:
    ...


def get_dataset(dataset_id: str) -> Result:
    ...


def search_datasets(query: str) -> Result:
    ...
