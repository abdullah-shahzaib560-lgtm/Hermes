from hermes.schemas.base import FieldDef, Schema

MARKET_OBSERVATION = Schema(
    name="market.observation",
    version="1.0.0",
    fields=[
        FieldDef(name="symbol", dtype="str", required=True),
        FieldDef(name="timestamp", dtype="datetime", required=True),
        FieldDef(name="open", dtype="float", nullable=True),
        FieldDef(name="high", dtype="float", nullable=True),
        FieldDef(name="low", dtype="float", nullable=True),
        FieldDef(name="close", dtype="float", nullable=True),
        FieldDef(name="volume", dtype="float", nullable=True),
        FieldDef(name="source", dtype="str", nullable=True),
    ],
    primary_keys=["symbol", "timestamp"],
    description="Canonical market observation (OHLCV).",
)
