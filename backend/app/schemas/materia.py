# Importa BaseModel para definir esquemas con Pydantic
from pydantic import BaseModel

# Importa UUID para identificadores únicos
from uuid import UUID


# Esquema para crear una materia
class MateriaCreate(BaseModel):

    # Nombre de la materia
    nombre: str

    # Número de créditos de la materia
    creditos: int

    # ID de la categoría a la que pertenece la materia
    id_categoria: UUID


# Esquema para leer una materia desde la base de datos
class MateriaRead(BaseModel):

    # ID único de la materia
    id_materia: UUID

    # Nombre de la materia
    nombre: str

    # Número de créditos
    creditos: int

    # ID de la categoría asociada
    id_categoria: UUID

    # Permite construir el modelo desde atributos ORM
    model_config = {"from_attributes": True}


# Esquema para actualizar una materia
class MateriaUpdate(BaseModel):

    # Nombre opcional
    nombre: str | None = None

    # Créditos opcionales
    creditos: int | None = None

    # Categoría opcional
    id_categoria: UUID | None = None