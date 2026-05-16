# Importa BaseModel para definir esquemas con Pydantic
from pydantic import BaseModel

# Importa UUID para identificadores únicos
from uuid import UUID

# Importa date para manejar fechas
from datetime import date


# Esquema para crear una relación estudiante-carrera
class EstudianteCarreraCreate(BaseModel):

    # ID del estudiante
    id_estudiante: UUID

    # ID de la carrera
    id_carrera: UUID

    # Semestre en el que se encuentra el estudiante
    semestre: str

    # Fecha de admisión a la carrera
    fecha_admision: date


# Esquema para leer la relación estudiante-carrera
class EstudianteCarreraRead(BaseModel):

    # ID del estudiante
    id_estudiante: UUID

    # ID de la carrera
    id_carrera: UUID

    # Semestre actual del estudiante
    semestre: str

    # Fecha de admisión
    fecha_admision: date

    # Permite construir el modelo desde atributos ORM
    model_config = {"from_attributes": True}


# Esquema para actualizar la relación estudiante-carrera
class EstudianteCarreraUpdate(BaseModel):

    # Semestre opcional
    semestre: str | None = None

    # Fecha de admisión opcional
    fecha_admision: date | None = None