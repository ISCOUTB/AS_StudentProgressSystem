from pydantic import BaseModel
from uuid import UUID
from datetime import date

class EstudianteCarreraCreate(BaseModel):
    id_estudiante: UUID
    id_carrera: UUID
    semestre: str
    fecha_admision: date

class EstudianteCarreraRead(BaseModel):
    id_estudiante: UUID
    id_carrera: UUID
    semestre: str
    fecha_admision: date

    model_config = {"from_attributes": True}

class EstudianteCarreraUpdate(BaseModel):
    semestre: str | None = None
    fecha_admision: date | None = None