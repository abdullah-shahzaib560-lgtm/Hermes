from typing import Any, Callable


class Paginator:

    def __init__(self, strategy: str = "page") -> None:
        self.strategy = strategy

    async def paginate(self, fetch_fn: Callable, **kwargs: Any) -> list:
        ...
