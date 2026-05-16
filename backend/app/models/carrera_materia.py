from sqlmodel import SQLModel, Relationship, Field
from typing import TYPE_CHECKING
import uuid

# TYPE_CHECKING evita importaciones circulares en tiempo de ejecución
if TYPE_CHECKING:
    from app.models.materia import Materias
    from app.models.carrera import Carreras

# Tabla intermedia que define la malla curricular (qué materias pertenecen a cada carrera)
class CarreraMateria(SQLModel, table=True):
    # Llave compuesta: una materia solo puede aparecer una vez por carrera
    id_materia: uuid.UUID = Field(foreign_key="materias.id_materia", primary_key=True)
    id_carrera: uuid.UUID = Field(foreign_key="carreras.id_carrera", primary_key=True)

    mat: "Materias" = Relationship(back_populates="cmat")
    car: "Carreras" = Relationship(back_populates="cmat")