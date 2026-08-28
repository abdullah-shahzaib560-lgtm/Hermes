from pydantic import BaseModel, Field
import uuid

from typing import NewType

from hermes.core.lineage import Lineage
from hermes.core.provenance import Provenance
from hermes.core.metadata import MetaData
from hermes.core.versioning import DataVersion


class Dataset(BaseModel):
    
    id: uuid.UUID = Field(default_factory=uuid.uuid4())
    name: str
    version: str

    schema_ref = ...
    metadata = MetaData()
    provenance = Provenance()
    lineage = Lineage()
