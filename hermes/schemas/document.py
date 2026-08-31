from hermes.schemas.base import FieldDef, Schema

DOCUMENT = Schema(
    name="document",
    version="1.0.0",
    fields=[
        FieldDef(name="document_id", dtype="str", required=True),
        FieldDef(name="title", dtype="str", nullable=True),
        FieldDef(name="source", dtype="str", required=True),
        FieldDef(name="date", dtype="datetime", nullable=True),
        FieldDef(name="url", dtype="str", nullable=True),
        FieldDef(name="content_type", dtype="str", nullable=True),
        FieldDef(name="metadata", dtype="dict", nullable=True),
    ],
    primary_keys=["document_id"],
    description="Canonical document/filing.",
)
