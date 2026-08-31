from pydantic import BaseModel
from typing import Callable


class FieldMapping(BaseModel):

    source_field: str
    target_field: str
    transform: Callable | None = None
    dtype: str | None = None
    default: object = None
