# Importa herramientas de FastAPI
from fastapi import APIRouter, Depends

# Importa Annotated para manejar dependencias tipadas
from typing import Annotated

# Importa la sesión de SQLModel para trabajar con la base de datos
from sqlmodel import Session

# Importa UUID para manejar identificadores únicos
from uuid import UUID

# Importa la función que proporciona la sesión de base de datos
from app.db.db import get_session

# Importa los esquemas de entrada y salida
# para la relación estudiante-carrera
from app.schemas.estudiante_carrera import (
    EstudianteCarreraCreate,
    EstudianteCarreraRead,
    EstudianteCarreraUpdate
)

# Importa los servicios relacionados con estudiante-carrera
from app.services import estudiante_carrera as service


# Crea el router para las rutas de estudiante-carrera
router = APIRouter(
    prefix="/estudiante-carrera",   # Prefijo base de las rutas
    tags=["Estudiante Carrera"]     # Etiqueta usada en Swagger
)


# Endpoint para obtener todas las carreras asociadas a un estudiante
@router.get("/{id_estudiante}", response_model=list[EstudianteCarreraRead])
def get_by_estudiante(
    id_estudiante: UUID,
    session: Annotated[Session, Depends(get_session)]
):
    
    # Llama al servicio que obtiene las carreras del estudiante
    return service.get_by_estudiante(session, id_estudiante)


# Endpoint para crear una nueva relación estudiante-carrera
@router.post("/", response_model=EstudianteCarreraRead, status_code=201)
def create(
    data: EstudianteCarreraCreate,
    session: Annotated[Session, Depends(get_session)]
):
    
    # Llama al servicio encargado de crear la relación
    return service.create(session, data)


# Endpoint para actualizar una relación estudiante-carrera
@router.patch("/{id_estudiante}/{id_carrera}", response_model=EstudianteCarreraRead)
def update(
    id_estudiante: UUID,
    id_carrera: UUID,
    data: EstudianteCarreraUpdate,
    session: Annotated[Session, Depends(get_session)]
):
    
    # Llama al servicio encargado de actualizar la relación
    return service.update(session, id_estudiante, id_carrera, data)


# Endpoint para eliminar una relación estudiante-carrera
@router.delete("/{id_estudiante}/{id_carrera}")
def delete(
    id_estudiante: UUID,
    id_carrera: UUID,
    session: Annotated[Session, Depends(get_session)]
):
    
    # Llama al servicio encargado de eliminar la relación
    return service.delete(session, id_estudiante, id_carrera)