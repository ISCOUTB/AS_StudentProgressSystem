from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING, Optional, List
import uuid

if TYPE_CHECKING:
    from app.models.logro_materia import LogroMaterias

class Logros(SQLModel, table=True):
    id_logro: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    nombre: str = Field(max_length=100)
    descripcion: str = Field(max_length=400)
    icon: str | None = Field(default=None, max_length=100)

    logro_mat: Optional[List["LogroMaterias"]] = Relationship(back_populates="log")