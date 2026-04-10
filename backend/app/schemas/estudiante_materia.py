from pydantic import BaseModel
from uuid import UUID
from app.enums.status_materia import StatusMaterias

class EstudianteMateriaCreate(BaseModel):
    id_estudiante: UUID
    id_materia: UUID
    status: StatusMaterias = StatusMaterias.encurso
    nota: float = 0.0
    semestre: str

class EstudianteMateriaRead(BaseModel):
    id_estudiante: UUID
    id_materia: UUID
    status: StatusMaterias
    nota: float
    semestre: str

    model_config = {"from_attributes": True}

class EstudianteMateriaUpdate(BaseModel):
    status: StatusMaterias | None = None
    nota: float | None = None
    semestre: str | None = None