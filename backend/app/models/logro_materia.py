from sqlmodel import SQLModel, Relationship, Field
import uuid
from typing import Optional

class LogroMaterias(SQLModel, table=True):
    id_logromateria: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key= True)
    id_logro: uuid.UUID = Field(foreign_key="log.id_logro")
    id_materia: uuid.UUID | None = Field(foreign_key="mat.id_materia")

    est_logro: Optional["EstudianteLogros"] = Relationship(back_populates="log_mat")
    log: "Logros" = Relationship(back_populates="logro_mat")  
    mat: "Materias" = Relationship(back_populates="log_mat")

