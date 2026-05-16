from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING, Optional, List
import uuid

if TYPE_CHECKING:
    from app.models.materia import Materias

class Categorias(SQLModel, table=True):
    """Categorías que agrupan materias (ej: Básicas, Profesionales)."""
    id_categoria: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    codigo: str = Field(max_length=4)
    nombre: str = Field(unique=True)

    # Materias que pertenecen a esta categoría
    mat: Optional[List["Materias"]] = Relationship(back_populates="cat")
