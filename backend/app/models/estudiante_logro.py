from sqlmodel import SQLModel, Relationship,Field
from enum.status_logro import StatusLogro
import uuid

class EstudianteLogros(SQLModel, table = True):
    staus: StatusLogro = Field(default=StatusLogro.noobtenido)
    id_estudiante: uuid.UUID = Field(foreign_key="estl.id_estudiante")
    id_logromateria: uuid.UUID = Field(foreign_key="log_mat.id_logromateria")
    

    estl: "Estudiantes" = Relationship(back_populates= "est_logro")
    log_mat: "LogroMaterias" = Relationship(back_populates="est_logro")
