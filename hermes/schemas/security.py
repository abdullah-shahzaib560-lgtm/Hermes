from hermes.schemas.base import FieldDef, Schema

SECURITY_EVENT = Schema(
    name="security.event",
    version="1.0.0",
    fields=[
        FieldDef(name="event_id", dtype="str", required=True),
        FieldDef(name="date", dtype="datetime", required=True),
        FieldDef(name="event_type", dtype="str", required=True),
        FieldDef(name="country", dtype="str", nullable=True),
        FieldDef(name="severity", dtype="str", nullable=True),
        FieldDef(name="description", dtype="str", nullable=True),
        FieldDef(name="source", dtype="str", nullable=True),
    ],
    primary_keys=["event_id"],
    description="Canonical security event.",
)
