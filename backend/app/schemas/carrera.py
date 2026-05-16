# Importa BaseModel para definir esquemas con Pydantic
from pydantic import BaseModel

# Importa UUID para identificar registros de forma única
from uuid import UUID

# Importa el enum de escuelas
from app.enums.escuela import Escuelas


# Esquema para crear una nueva carrera
class CarreraCreate(BaseModel):

    # Nombre de la carrera
    nombre: str

    # Código identificador de la carrera
    codigo: str

    # Escuela a la que pertenece la carrera (enum)
    escuela: Escuelas


# Esquema para leer una carrera desde la base de datos
class CarreraRead(BaseModel):

    # ID único de la carrera
    id_carrera: UUID

    # Nombre de la carrera
    nombre: str

    # Código de la carrera
    codigo: str

    # Escuela asociada
    escuela: Escuelas

    # Permite crear el modelo desde atributos de ORM
    model_config = {"from_attributes": True}


# Esquema para actualizar una carrera (campos opcionales)
class CarreraUpdate(BaseModel):

    # Nombre opcional
    nombre: str | None = None

    # Código opcional
    codigo: str | None = None

    # Escuela opcional
    escuela: Escuelas | None = None