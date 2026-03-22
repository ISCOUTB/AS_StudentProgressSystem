from sqlmodel import SQLModel, Field, Relationship
from enum.status_materia import StatusMaterias
import uuid

class EstudianteMateria(SQLModel, table= True):
    status: StatusMaterias = Field(default=StatusMaterias.encurso)
    nota: float = Field(le=5.0)
    semestre: str
    id_estudiante: uuid.UUID = Field(foreign_key="estm.id_estudiante")
    Id_materia: uuid.UUID = Field(foreign_key="mat.id_materia")

    estm: "Estudiantes" = Relationship(back_populates="est_mat")
    mat: "Materias" = Relationship(back_populates="est_mat")