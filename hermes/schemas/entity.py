from hermes.schemas.base import FieldDef, Schema

ENTITY = Schema(
    name="entity",
    version="1.0.0",
    fields=[
        FieldDef(name="entity_id", dtype="str", required=True),
        FieldDef(name="name", dtype="str", required=True),
        FieldDef(name="entity_type", dtype="str", required=True),
        FieldDef(name="country", dtype="str", nullable=True),
        FieldDef(name="identifiers", dtype="dict", nullable=True),
        FieldDef(name="aliases", dtype="list", nullable=True),
    ],
    primary_keys=["entity_id"],
    description="Canonical entity.",
)
