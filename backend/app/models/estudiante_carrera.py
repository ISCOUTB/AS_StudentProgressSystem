from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING
from datetime import date
import uuid

if TYPE_CHECKING:
    from app.models.estudiante import Estudiantes
    from app.models.carrera import Carreras

class EstudiantesCarreras(SQLModel, table=True):
    __tablename__ = "estudiantescarreras"

    id_estudiante: uuid.UUID = Field(foreign_key="estudiantes.id_estudiante", primary_key=True)
    id_carrera: uuid.UUID = Field(foreign_key="carreras.id_carrera", primary_key=True)
    semestre: str
    fecha_admision: date

    estc: "Estudiantes" = Relationship(back_populates="est_car")
    carr: "Carreras" = Relationship(back_populates="est_car")