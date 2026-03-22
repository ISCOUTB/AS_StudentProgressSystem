from sqlmodel import SQLModel, Field, Relationship
import uuid

class Categorias(SQLModel, table=True):
    id_categoria: uuid.UUID = Field(default_factory = uuid.uuid4, primary_key=True)
    codigo: str = Field(max_length=4)
    nombre: str = Field(unique=True)

    mat: "Materias" = Relationship(back_populates="cat") 