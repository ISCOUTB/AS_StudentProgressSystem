from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING, Optional, List
from pydantic import EmailStr
import uuid
from app.enums.status_estudiante import StatusEstudiante

if TYPE_CHECKING:
    from app.models.estudiante_carrera import EstudiantesCarreras
    from app.models.estudiante_materia import EstudianteMateria
    from app.models.estudiante_logro import EstudianteLogros

class Estudiantes(SQLModel, table=True):
    id_estudiante: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    nombre: str = Field(max_length=100)
    apellido: str = Field(max_length=100)
    codigo: str = Field(max_length=9, unique=True)
    correo: EmailStr = Field(unique=True, max_length=100, index=True)
    status: StatusEstudiante = Field(default=StatusEstudiante.activo)
    hash_password: str

    est_car: Optional[List["EstudiantesCarreras"]] = Relationship(back_populates="estc")
    est_mat: Optional[List["EstudianteMateria"]] = Relationship(back_populates="estm")
    est_logro: Optional[List["EstudianteLogros"]] = Relationship(back_populates="estl")