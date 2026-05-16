# Importa herramientas principales de FastAPI
from fastapi import APIRouter, Depends, HTTPException

# Importa la sesión de SQLModel para acceder a la base de datos
from sqlmodel import Session

# Importa Annotated para tipado de dependencias
from typing import Annotated

# Importa UUID para manejo de identificadores únicos
from uuid import UUID

# Importa la función que genera la sesión de base de datos
from app.db.db import get_session

# Importa los esquemas de estudiante
from app.schemas.estudiante import (
    EstudianteCreate,
    EstudianteRead,
    EstudianteUpdate
)

# Importa los servicios de estudiante
from app.services import estudiante as service

# Importa el modelo de estudiantes (aunque aquí no se usa directamente)
from app.models.estudiante import Estudiantes

# Importa dependencia del usuario autenticado
from app.deps import CurrentUser


# Crea el router para las rutas de estudiantes
router = APIRouter(
    prefix="/estudiantes",   # Prefijo base de las rutas
    tags=["Estudiantes"]     # Etiqueta para documentación Swagger
)


# Endpoint para obtener los datos del usuario autenticado
@router.get("/me", response_model=EstudianteRead)
def get_me(current_user: CurrentUser):

    # Intenta obtener el estudiante asociado al usuario autenticado
    # ⚠️ Nota: aquí debería llamarse al servicio con session si se necesita DB
    return get_by_id(current_user.id_estudiante)


# Endpoint para obtener todos los estudiantes
@router.get("/", response_model=list[EstudianteRead])
def get_all(
    session: Annotated[Session, Depends(get_session)]
):
    
    # Llama al servicio para obtener todos los estudiantes
    return service.get_all(session)


# Endpoint para obtener un estudiante por ID
@router.get("/{id_estudiante}", response_model=EstudianteRead)
def get_by_id(
    id_estudiante: UUID,
    session: Annotated[Session, Depends(get_session)]
):
    
    # Llama al servicio que busca el estudiante por ID
    return service.get_by_id(session, id_estudiante)


# Endpoint para crear un nuevo estudiante
@router.post("/", response_model=EstudianteRead, status_code=201)
def create(
    data: EstudianteCreate,
    session: Annotated[Session, Depends(get_session)]
):
    
    # Llama al servicio encargado de crear el estudiante
    return service.create(session, data)


# Endpoint para actualizar un estudiante existente
@router.patch("/{id_estudiante}", response_model=EstudianteRead)
def update(
    id_estudiante: UUID,
    data: EstudianteUpdate,
    session: Annotated[Session, Depends(get_session)]
):
    
    # Llama al servicio encargado de actualizar el estudiante
    return service.update(session, id_estudiante, data)


# Endpoint para eliminar un estudiante
@router.delete("/{id_estudiante}")
def delete(
    id_estudiante: UUID,
    session: Annotated[Session, Depends(get_session)]
):
    
    # Llama al servicio encargado de eliminar el estudiante
    return service.delete(session, id_estudiante)