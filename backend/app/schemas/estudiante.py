from pydantic import BaseModel, EmailStr
from uuid import UUID
from app.enums.status_estudiante import StatusEstudiante

class EstudianteCreate(BaseModel):
    nombre: str
    apellido: str
    codigo: str
    correo: EmailStr
    password: str
    status: StatusEstudiante = StatusEstudiante.activo

class EstudianteRead(BaseModel):
    id_estudiante: UUID
    nombre: str
    apellido: str
    codigo: str
    correo: EmailStr
    status: StatusEstudiante

    model_config = {"from_attributes": True}

class EstudianteUpdate(BaseModel):
    nombre: str | None = None
    apellido: str | None = None
    correo: EmailStr | None = None
    status: StatusEstudiante | None = None