# Importa BaseModel para definir esquemas con Pydantic
from pydantic import BaseModel

# Importa UUID para identificadores únicos
from uuid import UUID


# Esquema para crear una relación logro-materia
class LogroMateriaCreate(BaseModel):

    # ID del logro
    id_logro: UUID

    # ID de la materia (opcional)
    id_materia: UUID | None = None


# Esquema para leer la relación logro-materia
class LogroMateriaRead(BaseModel):

    # ID de la relación logro-materia
    id_logromateria: UUID

    # ID del logro
    id_logro: UUID

    # ID de la materia (puede ser nulo)
    id_materia: UUID | None = None

    # Permite construir el modelo desde atributos ORM
    model_config = {"from_attributes": True}