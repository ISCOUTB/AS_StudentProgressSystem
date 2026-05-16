
# Importa BaseModel para definir esquemas con Pydantic
from pydantic import BaseModel

# Importa UUID para identificadores únicos
from uuid import UUID

# Importa el enum de estado del logro
from app.enums.status_logro import StatusLogro


# Esquema para crear una relación estudiante-logro
class EstudianteLogroCreate(BaseModel):

    # ID del estudiante
    id_estudiante: UUID

    # ID del logro-materia
    id_logromateria: UUID

    # Estado del logro (por defecto: no obtenido)
    status: StatusLogro = StatusLogro.noobtenido


# Esquema para leer la relación estudiante-logro
class EstudianteLogroRead(BaseModel):

    # ID del estudiante
    id_estudiante: UUID

    # ID del logro-materia
    id_logromateria: UUID

    # Estado del logro
    status: StatusLogro

    # Permite crear el modelo desde atributos ORM
    model_config = {"from_attributes": True}


# Esquema para actualizar el estado del logro del estudiante
class EstudianteLogroUpdate(BaseModel):

    # Estado opcional del logro
    status: StatusLogro | None = None

