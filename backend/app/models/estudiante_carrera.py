from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING
from datetime import date
import uuid

# TYPE_CHECKING evita importaciones circulares en tiempo de ejecución
if TYPE_CHECKING:
    from app.models.estudiante import Estudiantes
    from app.models.carrera import Carreras

# Matrícula de un estudiante en una carrera (llave compuesta)
class EstudiantesCarreras(SQLModel, table=True):
    __tablename__ = "estudiantescarreras"

    # Llave compuesta: un estudiante solo puede matricularse una vez por carrera
    id_estudiante: uuid.UUID = Field(foreign_key="estudiantes.id_estudiante", primary_key=True)
    id_carrera: uuid.UUID = Field(foreign_key="carreras.id_carrera", primary_key=True)
    semestre: str        # Semestre de ingreso, ej: "2024-1"
    fecha_admision: date

    estc: "Estudiantes" = Relationship(back_populates="est_car")
    carr: "Carreras" = Relationship(back_populates="est_car")