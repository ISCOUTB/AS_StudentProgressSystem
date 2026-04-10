from pydantic import BaseModel
from uuid import UUID

class LogroMateriaCreate(BaseModel):
    id_logro: UUID
    id_materia: UUID | None = None

class LogroMateriaRead(BaseModel):
    id_logromateria: UUID
    id_logro: UUID
    id_materia: UUID | None = None

    model_config = {"from_attributes": True}