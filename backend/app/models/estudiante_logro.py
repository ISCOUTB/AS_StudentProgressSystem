from sqlmodel import SQLModel, Relationship, Field
from typing import TYPE_CHECKING
from app.enums.status_logro import StatusLogro
import uuid

# TYPE_CHECKING evita importaciones circulares en tiempo de ejecución
if TYPE_CHECKING:
    from app.models.estudiante import Estudiantes
    from app.models.logro_materia import LogroMaterias

# Registro del estado de un logro específico para un estudiante (llave compuesta)
class EstudianteLogros(SQLModel, table=True):
    __tablename__ = "estudiantelogros"

    id_estudiante: uuid.UUID = Field(foreign_key="estudiantes.id_estudiante", primary_key=True)
    id_logromateria: uuid.UUID = Field(foreign_key="logromaterias.id_logromateria", primary_key=True)
    status: StatusLogro = Field(default=StatusLogro.noobtenido)  # Por defecto: no obtenido

    estl: "Estudiantes" = Relationship(back_populates="est_logro")
    log_mat: "LogroMaterias" = Relationship(back_populates="est_logro")