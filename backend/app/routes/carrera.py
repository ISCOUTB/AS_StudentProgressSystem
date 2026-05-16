# Importa Annotated para tipado avanzado con dependencias
from typing import Annotated

# Importa herramientas de FastAPI
from fastapi import APIRouter, Depends

# Importa la sesión para trabajar con la base de datos
from sqlmodel import Session

# Importa UUID para manejar identificadores únicos
from uuid import UUID

# Importa la función que genera la sesión de base de datos
from app.db.db import get_session

# Importa los esquemas de entrada y salida para carreras
from app.schemas.carrera import (
    CarreraCreate,
    CarreraRead,
    CarreraUpdate
)

# Importa los servicios relacionados con carreras
from app.services import carrera as service


# Crea el router para las rutas de carreras
router = APIRouter(
    prefix="/carreras",   # Prefijo base de las rutas
    tags=["Carreras"]     # Etiqueta para la documentación Swagger
)


# Endpoint para obtener todas las carreras
@router.get("/", response_model=list[CarreraRead])
def get_all(
    session: Annotated[Session, Depends(get_session)]
):
    
    # Llama al servicio que obtiene todas las carreras
    return service.get_all(session)


# Endpoint para obtener una carrera por ID
@router.get("/{id_carrera}", response_model=CarreraRead)
def get_by_id(
    id_carrera: UUID,
    session: Annotated[Session, Depends(get_session)]
):
    
    # Llama al servicio para buscar la carrera por ID
    return service.get_by_id(session, id_carrera)


# Endpoint para crear una nueva carrera
@router.post("/", response_model=CarreraRead, status_code=201)
def create(
    data: CarreraCreate,
    session: Annotated[Session, Depends(get_session)]
):
    
    # Llama al servicio que crea la carrera
    return service.create(session, data)


# Endpoint para actualizar una carrera existente
@router.patch("/{id_carrera}", response_model=CarreraRead)
def update(
    id_carrera: UUID,
    data: CarreraUpdate,
    session: Annotated[Session, Depends(get_session)]
):
    
    # Llama al servicio para actualizar la carrera
    return service.update(session, id_carrera, data)


# Endpoint para eliminar una carrera
@router.delete("/{id_carrera}")
def delete(
    id_carrera: UUID,
    session: Annotated[Session, Depends(get_session)]
):
    
    # Llama al servicio para eliminar la carrera
    return service.delete(session, id_carrera)