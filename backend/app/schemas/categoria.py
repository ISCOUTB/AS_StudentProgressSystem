# Importa BaseModel para crear esquemas con Pydantic
from pydantic import BaseModel

# Importa UUID para manejar identificadores únicos
from uuid import UUID


# Esquema para crear una categoría
class CategoriaCreate(BaseModel):

    # Código identificador de la categoría
    codigo: str

    # Nombre de la categoría
    nombre: str


# Esquema para leer una categoría desde la base de datos
class CategoriaRead(BaseModel):

    # ID único de la categoría
    id_categoria: UUID

    # Código de la categoría
    codigo: str

    # Nombre de la categoría
    nombre: str

    # Permite crear el modelo desde atributos de ORM
    model_config = {"from_attributes": True}


# Esquema para actualizar una categoría (campos opcionales)
class CategoriaUpdate(BaseModel):

    # Código opcional
    codigo: str | None = None

    # Nombre opcional
    nombre: str | None = None