from sqlmodel import SQLModel, Relationship, Field
from typing import TYPE_CHECKING
from app.enums.status_logro import StatusLogro
import uuid

if TYPE_CHECKING:
    from app.models.estudiante import Estudiantes
    from app.models.logro_materia import LogroMaterias

class EstudianteLogros(SQLModel, table=True):
    __tablename__ = "estudiantelogros"

    id_estudiante: uuid.UUID = Field(foreign_key="estudiantes.id_estudiante", primary_key=True)
    id_logromateria: uuid.UUID = Field(foreign_key="logromaterias.id_logromateria", primary_key=True)
    status: StatusLogro = Field(default=StatusLogro.noobtenido)

    estl: "Estudiantes" = Relationship(back_populates="est_logro")
    log_mat: "LogroMaterias" = Relationship(back_populates="est_logro")