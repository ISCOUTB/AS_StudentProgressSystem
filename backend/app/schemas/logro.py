
# Importa BaseModel para definir esquemas con Pydantic
from pydantic import BaseModel

# Importa UUID para identificadores únicos
from uuid import UUID


# Esquema para crear un logro
class LogroCreate(BaseModel):

    # Nombre del logro
    nombre: str

    # Descripción del logro
    descripcion: str

    # Icono del logro (opcional)
    icon: str | None = None


# Esquema para leer un logro desde la base de datos
class LogroRead(BaseModel):

    # ID único del logro
    id_logro: UUID

    # Nombre del logro
    nombre: str

    # Descripción del logro
    descripcion: str

    # Icono del logro (opcional)
    icon: str | None = None

    # Permite construir el modelo desde atributos ORM
    model_config = {"from_attributes": True}


# Esquema para actualizar un logro
class LogroUpdate(BaseModel):

    # Nombre opcional
    nombre: str | None = None

    # Descripción opcional
    descripcion: str | None = None

    # Icono opcional
    icon: str | None = None

