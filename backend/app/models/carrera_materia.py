from sqlmodel import SQLModel, Relationship, Field
from typing import TYPE_CHECKING
import uuid

if TYPE_CHECKING:
    from app.models.materia import Materias
    from app.models.carrera import Carreras

class CarreraMateria(SQLModel, table=True):
    id_materia: uuid.UUID = Field(foreign_key="materias.id_materia", primary_key=True)
    id_carrera: uuid.UUID = Field(foreign_key="carreras.id_carrera", primary_key=True)

    mat: "Materias" = Relationship(back_populates="cmat")
    car: "Carreras" = Relationship(back_populates="cmat")