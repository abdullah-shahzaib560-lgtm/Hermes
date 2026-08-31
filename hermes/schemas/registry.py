from hermes.schemas.base import Schema


class SchemaRegistry:

    def __init__(self) -> None:
        self._schemas: dict[str, dict[str, Schema]] = {}

    def register(self, schema: Schema) -> None:
        ...

    def get(self, name: str, version: str | None = None) -> Schema | None:
        ...

    def list(self) -> list[Schema]:
        ...

    def list_names(self) -> list[str]:
        ...

    def migrate(self, data: object, from_schema: Schema, to_schema: Schema) -> object:
        ...
