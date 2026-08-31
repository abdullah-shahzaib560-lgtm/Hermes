from hermes.schemas.base import FieldDef, Schema

FINANCIAL_OBSERVATION = Schema(
    name="financial.observation",
    version="1.0.0",
    fields=[
        FieldDef(name="entity_id", dtype="str", required=True),
        FieldDef(name="date", dtype="datetime", required=True),
        FieldDef(name="metric", dtype="str", required=True),
        FieldDef(name="value", dtype="float", nullable=True),
        FieldDef(name="unit", dtype="str", nullable=True),
        FieldDef(name="period", dtype="str", nullable=True),
        FieldDef(name="source", dtype="str", nullable=True),
    ],
    primary_keys=["entity_id", "date", "metric"],
    description="Canonical financial observation.",
)
