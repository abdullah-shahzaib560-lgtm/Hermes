from hermes.core.result import Result


def resolve_entity(query: str, entity_type: str | None = None) -> Result:
    ...


def resolve_country(query: str) -> Result:
    ...


def resolve_company(query: str) -> Result:
    ...
