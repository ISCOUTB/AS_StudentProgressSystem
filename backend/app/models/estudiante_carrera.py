from sqlmodel import SQLModel, Field, Relationship
from datetime import date
import uuid

class EstudiantesCarreras(SQLModel, table=True):
    semestre: str 
    fechaadmision : date

    id_estudiante: uuid.UUID = Field(foreign_key="estc.id_estudiante")
    id_carrera: uuid.UUID = Field(foreign_key="carr.id_carrera")
    

    estc: "Estudiantes" = Relationship(back_populates= "est_Car")
    carr: "Carreras" = Relationship(back_populates="st_Car")

