from pydantic import BaseModel
from uuid import UUID
from app.schemas.materia import MateriaRead

class MallaCreate(BaseModel):
    id_carrera: UUID
    id_materia: UUID

class MallaRead(BaseModel):
    id_carrera: UUID
    id_materia: UUID

    model_config = {"from_attributes": True}

class MallaCompletaRead(BaseModel):
    id_carrera: UUID
    nombre: str
    codigo: str
    materias: list[MateriaRead]

    model_config = {"from_attributes": True}