from pydantic import BaseModel
from uuid import UUID

class CategoriaCreate(BaseModel):
    codigo: str
    nombre: str

class CategoriaRead(BaseModel):
    id_categoria: UUID
    codigo: str
    nombre: str

    model_config = {"from_attributes": True}

class CategoriaUpdate(BaseModel):
    codigo: str | None = None
    nombre: str | None = None