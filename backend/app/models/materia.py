from sqlmodel import SQLModel, Field, Relationship
import uuid
from typing import Optional
class Materias(SQLModel, table=True):
    id_materia: uuid.UUID = Field(default_factory= uuid.uuid4, primary_key=True)
    nombre: str = Field(max_length=100)
    creditos: int = Field(le=9)
    id_categoria: uuid.UUID = Field(foreign_key="cat.id_categoria")
    
    cat: "Categorias" = Relationship(back_populates="mat") 
    log_mat: Optional["LogroMaterias"] = Relationship(back_populates= "mat")
    est_mat: Optional["EstudianteMaterias"] = Relationship(back_populates="mat")
    cmat: Optional["CarreraMaterias"] = Relationship(back_populates="mat")