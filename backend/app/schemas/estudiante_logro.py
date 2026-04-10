from pydantic import BaseModel
from uuid import UUID
from app.enums.status_logro import StatusLogro

class EstudianteLogroCreate(BaseModel):
    id_estudiante: UUID
    id_logromateria: UUID
    status: StatusLogro = StatusLogro.noobtenido

class EstudianteLogroRead(BaseModel):
    id_estudiante: UUID
    id_logromateria: UUID
    status: StatusLogro

    model_config = {"from_attributes": True}

class EstudianteLogroUpdate(BaseModel):
    status: StatusLogro | None = None