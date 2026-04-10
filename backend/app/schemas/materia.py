from pydantic import BaseModel
from uuid import UUID

class MateriaCreate(BaseModel):
    nombre: str
    creditos: int
    id_categoria: UUID

class MateriaRead(BaseModel):
    id_materia: UUID
    nombre: str
    creditos: int
    id_categoria: UUID

    model_config = {"from_attributes": True}

class MateriaUpdate(BaseModel):
    nombre: str | None = None
    creditos: int | None = None
    id_categoria: UUID | None = None