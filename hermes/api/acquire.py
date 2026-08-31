from hermes.core.result import Result


def fetch(source: str, **kwargs: object) -> Result:
    ...


def ingest(source: str, **kwargs: object) -> Result:
    ...


def read(path: str, **kwargs: object) -> Result:
    ...


def sync(source: str, **kwargs: object) -> Result:
    ...
