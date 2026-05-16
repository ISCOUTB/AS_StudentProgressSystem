# Importa BaseModel para definir esquemas con Pydantic
from pydantic import BaseModel

# Importa UUID para identificadores únicos
from uuid import UUID

# Importa el esquema de lectura de Materia
from app.schemas.materia import MateriaRead


# Esquema para crear una relación de malla curricular
class MallaCreate(BaseModel):

    # ID de la carrera
    id_carrera: UUID

    # ID de la materia
    id_materia: UUID


# Esquema para leer una relación simple de malla
class MallaRead(BaseModel):

    # ID de la carrera
    id_carrera: UUID

    # ID de la materia
    id_materia: UUID

    # Permite construir el modelo desde atributos ORM
    model_config = {"from_attributes": True}


# Esquema para leer una malla completa (carrera + materias)
class MallaCompletaRead(BaseModel):

    # ID de la carrera
    id_carrera: UUID

    # Nombre de la carrera
    nombre: str

    # Código de la carrera
    codigo: str

    # Lista de materias asociadas a la carrera
    materias: list[MateriaRead]

    # Permite construir el modelo desde atributos ORM
    model_config = {"from_attributes": True}