from sqlmodel import SQLModel, Field, Relationship
import uuid
from typing import Optional

class Logros(SQLModel, table=True):
    id_logro: uuid.UUID = Field(default_factory= uuid.uuid4, primary_key=True)
    nombre: str = Field(max_length=100)
    descripcion: str = Field(max_length=400)


    logro_mat: Optional["LogroMaterias"] = Relationship(back_populates="log")
    