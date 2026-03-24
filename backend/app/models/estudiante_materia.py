from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING
from app.enums.status_materia import StatusMaterias
import uuid

if TYPE_CHECKING:
    from app.models.estudiante import Estudiantes
    from app.models.materia import Materias

class EstudianteMateria(SQLModel, table=True):
    __tablename__ = "estudiantemateria"

    id_estudiante: uuid.UUID = Field(foreign_key="estudiantes.id_estudiante", primary_key=True)
    id_materia: uuid.UUID = Field(foreign_key="materias.id_materia", primary_key=True)
    status: StatusMaterias = Field(default=StatusMaterias.encurso)
    nota: float = Field(default=0.0, ge=0.0, le=5.0)
    semestre: str

    estm: "Estudiantes" = Relationship(back_populates="est_mat")
    mat: "Materias" = Relationship(back_populates="est_mat")