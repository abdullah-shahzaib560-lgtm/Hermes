from pydantic import BaseModel


class Expression(BaseModel):

    operator: str
    operands: list[object] = []


def and_(*filters: object) -> Expression:
    ...


def or_(*filters: object) -> Expression:
    ...


def not_(filter_obj: object) -> Expression:
    ...
