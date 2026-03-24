from sqlmodel import SQLModel, Relationship, Field
from typing import TYPE_CHECKING, Optional, List
import uuid

if TYPE_CHECKING:
    from app.models.logro import Logros
    from app.models.materia import Materias
    from app.models.estudiante_logro import EstudianteLogros

class LogroMaterias(SQLModel, table=True):
    __tablename__ = "logromaterias"

    id_logromateria: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    id_logro: uuid.UUID = Field(foreign_key="logros.id_logro")
    id_materia: uuid.UUID | None = Field(foreign_key="materias.id_materia", default=None)

    est_logro: Optional[List["EstudianteLogros"]] = Relationship(back_populates="log_mat")
    log: "Logros" = Relationship(back_populates="logro_mat")
    mat: "Materias" = Relationship(back_populates="log_mat")