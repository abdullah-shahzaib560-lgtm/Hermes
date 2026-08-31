from hermes.core.result import Result


def get_schema(name: str, version: str | None = None) -> Result:
    ...


def register_schema(schema: object) -> Result:
    ...


def compare_schema(schema_a: object, schema_b: object) -> Result:
    ...


def migrate(data: object, from_schema: object, to_schema: object) -> Result:
    ...
