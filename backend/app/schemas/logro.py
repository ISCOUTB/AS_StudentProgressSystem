from pydantic import BaseModel
from uuid import UUID

class LogroCreate(BaseModel):
    nombre: str
    descripcion: str
    icon: str | None = None

class LogroRead(BaseModel):
    id_logro: UUID
    nombre: str
    descripcion: str
    icon: str | None = None

    model_config = {"from_attributes": True}

class LogroUpdate(BaseModel):
    nombre: str | None = None
    descripcion: str | None = None
    icon: str | None = None