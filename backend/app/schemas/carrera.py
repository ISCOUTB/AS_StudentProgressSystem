from pydantic import BaseModel
from uuid import UUID
from app.enums.escuela import Escuelas

class CarreraCreate(BaseModel):
    nombre: str
    codigo: str
    escuela: Escuelas

class CarreraRead(BaseModel):
    id_carrera: UUID
    nombre: str
    codigo: str
    escuela: Escuelas

    model_config = {"from_attributes": True}

class CarreraUpdate(BaseModel):
    nombre: str | None = None
    codigo: str | None = None
    escuela: Escuelas | None = None