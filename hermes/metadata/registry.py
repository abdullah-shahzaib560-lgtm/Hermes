class MetadataRegistry:

    def __init__(self) -> None:
        self._extractors: dict[str, object] = {}

    def register(self, name: str, extractor: object) -> None:
        ...

    def get(self, name: str) -> object | None:
        ...

    def list(self) -> list[str]:
        ...
