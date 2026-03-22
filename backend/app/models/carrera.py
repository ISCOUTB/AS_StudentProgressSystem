from sqlmodel import SQLModel, Field, Relationship
import uuid
from enum.escuela import Escuelas
from typing import Optional

class Carreras(SQLModel, table=True):
    id_carrera: uuid.UUID = Field(default_factory = uuid.uuid4, primary_key=True)
    nombre: str = Field(max_length=100)
    codigo: str = Field(max_length=4)
    escuela: Escuelas  

    cmat: Optional["CarreraMaterias"] = Relationship(back_populates="car")
