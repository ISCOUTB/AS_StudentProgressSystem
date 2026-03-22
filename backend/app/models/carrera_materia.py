from sqlmodel import SQLModel, Relationship, Field
import uuid

class CarreraMateria(SQLModel, table = True):
    id_materia: uuid.UUID = Field(foreign_key="mat.id_materia")
    id_carrera: uuid.UUID = Field(foreign_key="car.id_carrera")



    mat:"Materias" = Relationship(back_populates="cmat")
    car: "Carreras" = Relationship(back_populates="cmat")