from pydantic import BaseModel


class Filter(BaseModel):

    field: str
    operator: str
    value: object


def eq(field: str, value: object) -> Filter:
    ...


def gt(field: str, value: object) -> Filter:
    ...


def lt(field: str, value: object) -> Filter:
    ...


def gte(field: str, value: object) -> Filter:
    ...


def lte(field: str, value: object) -> Filter:
    ...


def in_list(field: str, values: list[object]) -> Filter:
    ...


def between(field: str, low: object, high: object) -> Filter:
    ...
