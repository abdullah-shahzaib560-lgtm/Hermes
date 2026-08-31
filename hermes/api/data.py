from hermes.core.result import Result


def parse(data: object, **kwargs: object) -> Result:
    ...


def normalize(data: object, **kwargs: object) -> Result:
    ...


def validate(data: object, contract: object | None = None) -> Result:
    ...


def transform(data: object, fn: object | None = None, **kwargs: object) -> Result:
    ...


def profile(data: object) -> Result:
    ...


def inspect(data: object) -> Result:
    ...
