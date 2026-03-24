from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING, Optional, List
import uuid

if TYPE_CHECKING:
    from app.models.categorias import Categorias
    from app.models.logro_materia import LogroMaterias
    from app.models.estudiante_materia import EstudianteMateria
    from app.models.carrera_materia import CarreraMateria

class Materias(SQLModel, table=True):
    id_materia: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    nombre: str = Field(max_length=100)
    creditos: int = Field(ge=1, le=9)
    id_categoria: uuid.UUID = Field(foreign_key="categorias.id_categoria")

    cat: "Categorias" = Relationship(back_populates="mat")
    log_mat: Optional[List["LogroMaterias"]] = Relationship(back_populates="mat")
    est_mat: Optional[List["EstudianteMateria"]] = Relationship(back_populates="mat")
    cmat: Optional[List["CarreraMateria"]] = Relationship(back_populates="mat")