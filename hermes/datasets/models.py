from pydantic import BaseModel


class DatasetDescriptor(BaseModel):

    id: str
    name: str
    description: str = ""
    source: str = ""
    schema: object | None = None
    coverage: str | None = None
    frequency: str | None = None
    version: str = "0.0.1"
    quality: str | None = None
