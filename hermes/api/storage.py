from hermes.core.result import Result


def save(data: object, path: str, format: str = "parquet") -> Result:
    ...


def load(path: str) -> Result:
    ...


def query(data: object, **kwargs: object) -> Result:
    ...


def materialize(data: object, target: str) -> Result:
    ...
