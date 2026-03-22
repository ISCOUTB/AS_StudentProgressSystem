from sqlmodel import SQLModel, Field, Relationship
from pydantic import EmailStr
import uuid
from enum.status_estudiante import StatusEstudiante
from typing import Optional


class Estudiantes(SQLModel, table=True):

    id_estudiante: uuid.UUID = Field(default_factory= uuid.uuid4, primary_key=True)
    nombre: str = Field(max_length=100)
    apellido: str = Field(max_length=100)
    codigo: str = Field(max_length=9, unique=True)
    correo: EmailStr = Field(unique=True, max_length=100, index=True)
    status: StatusEstudiante = Field(default=StatusEstudiante.activo)
    hash_password: str 

    est_car: Optional["EstudiantesCarreras"] = Relationship(back_populates = "estc")
    est_mat: Optional["EstudianteMaterias"] = Relationship(back_populates= "estm")
    est_logro: Optional["EstudianteLogros"] = Relationship(back_populates="estl")

    