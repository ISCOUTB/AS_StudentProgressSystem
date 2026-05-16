# Importa BaseModel para definir esquemas con Pydantic
from pydantic import BaseModel, EmailStr

# Importa UUID para identificadores únicos
from uuid import UUID

# Importa el enum de estado del estudiante
from app.enums.status_estudiante import StatusEstudiante


# Esquema para crear un estudiante
class EstudianteCreate(BaseModel):

    # Nombre del estudiante
    nombre: str

    # Apellido del estudiante
    apellido: str

    # Código único del estudiante
    codigo: str

    # Correo electrónico con validación de formato
    correo: EmailStr

    # Contraseña del estudiante
    password: str

    # Estado del estudiante (por defecto activo)
    status: StatusEstudiante = StatusEstudiante.activo


# Esquema para leer un estudiante desde la base de datos
class EstudianteRead(BaseModel):

    # ID único del estudiante
    id_estudiante: UUID

    # Nombre del estudiante
    nombre: str

    # Apellido del estudiante
    apellido: str

    # Código del estudiante
    codigo: str

    # Correo electrónico
    correo: EmailStr

    # Estado del estudiante
    status: StatusEstudiante

    # Permite construir el modelo desde ORM
    model_config = {"from_attributes": True}


# Esquema para actualizar un estudiante
class EstudianteUpdate(BaseModel):

    # Nombre opcional
    nombre: str | None = None

    # Apellido opcional
    apellido: str | None = None

    # Correo opcional con validación
    correo: EmailStr | None = None

    # Estado opcional
    status: StatusEstudiante | None = None