from datetime import datetime

from pydantic import BaseModel, Field


class LineageStep(BaseModel):

    operation: str
    input_ref: str | None = None
    output_ref: str | None = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    params: dict = {}
    component_version: str | None = None


class Lineage(BaseModel):

    steps: list[LineageStep] = []

    def add_step(self, step: LineageStep) -> None:
        ...

    def trace(self) -> list[LineageStep]:
        ...

    def last_operation(self) -> LineageStep | None:
        ...
