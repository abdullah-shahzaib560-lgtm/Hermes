from typing import Any, Literal

from pydantic import BaseModel

from hermes.core.errors import HermesError


class Result(BaseModel):

    status: Literal["success", "warning", "partial", "failure"]
    data: Any = None
    errors: list[HermesError] = []
    warnings: list[str] = []

    def is_success(self) -> bool:
        ...

    def is_failure(self) -> bool:
        ...

    def raise_if_failure(self) -> None:
        ...
