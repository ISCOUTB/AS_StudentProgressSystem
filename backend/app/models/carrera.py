from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING, Optional, List
import uuid
from app.enums.escuela import Escuelas

if TYPE_CHECKING:
    from app.models.carrera_materia import CarreraMateria
    from app.models.estudiante_carrera import EstudiantesCarreras

class Carreras(SQLModel, table=True):
    """Tabla de carreras académicas."""
    id_carrera: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    nombre: str = Field(max_length=100)
    codigo: str = Field(max_length=4)       # Código corto de la carrera (ej: "INGE")
    escuela: Escuelas                        # Escuela a la que pertenece

    # Relación con la malla (materias de la carrera)
    cmat: Optional[List["CarreraMateria"]] = Relationship(back_populates="car")
    # Relación con los estudiantes matriculados en esta carrera
    est_car: Optional[List["EstudiantesCarreras"]] = Relationship(back_populates="carr")
