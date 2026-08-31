from hermes.schemas.base import FieldDef, Schema

ECONOMIC_OBSERVATION = Schema(
    name="economic.observation",
    version="1.0.0",
    fields=[
        FieldDef(name="entity_id", dtype="str", required=True),
        FieldDef(name="date", dtype="datetime", required=True),
        FieldDef(name="indicator", dtype="str", required=True),
        FieldDef(name="value", dtype="float", nullable=True),
        FieldDef(name="unit", dtype="str", nullable=True),
        FieldDef(name="frequency", dtype="str", nullable=True),
        FieldDef(name="source", dtype="str", nullable=True),
    ],
    primary_keys=["entity_id", "date", "indicator"],
    description="Canonical economic observation.",
)
