from hermes.schemas.base import FieldDef, Schema

GEOPOLITICAL_EVENT = Schema(
    name="geopolitical.event",
    version="1.0.0",
    fields=[
        FieldDef(name="event_id", dtype="str", required=True),
        FieldDef(name="date", dtype="datetime", required=True),
        FieldDef(name="event_type", dtype="str", required=True),
        FieldDef(name="actor_1", dtype="str", nullable=True),
        FieldDef(name="actor_2", dtype="str", nullable=True),
        FieldDef(name="country", dtype="str", nullable=True),
        FieldDef(name="goldstein_scale", dtype="float", nullable=True),
        FieldDef(name="source", dtype="str", nullable=True),
    ],
    primary_keys=["event_id"],
    description="Canonical geopolitical event.",
)
