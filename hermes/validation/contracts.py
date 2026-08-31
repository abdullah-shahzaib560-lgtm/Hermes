from pydantic import BaseModel


class Constraint(BaseModel):

    field: str
    constraint_type: str
    params: dict = {}


class DataContract(BaseModel):

    schema: object | None = None
    required_columns: list[str] = []
    constraints: list[Constraint] = []
    description: str | None = None
