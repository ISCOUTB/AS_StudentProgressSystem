from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING, Optional, List
import uuid
from app.enums.escuela import Escuelas

if TYPE_CHECKING:
    from app.models.carrera_materia import CarreraMateria
    from app.models.estudiante_carrera import EstudiantesCarreras

class Carreras(SQLModel, table=True):
    id_carrera: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    nombre: str = Field(max_length=100)
    codigo: str = Field(max_length=4)
    escuela: Escuelas

    cmat: Optional[List["CarreraMateria"]] = Relationship(back_populates="car")
    est_car: Optional[List["EstudiantesCarreras"]] = Relationship(back_populates="carr")