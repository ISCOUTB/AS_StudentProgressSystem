# Importa herramientas principales de FastAPI
from fastapi import APIRouter, Depends

# Importa la sesión de SQLModel para interactuar con la base de datos
from sqlmodel import Session

# Importa UUID para manejo de identificadores únicos
from uuid import UUID

# Importa Annotated para tipado de dependencias
from typing import Annotated

# Importa la función que genera la sesión de base de datos
from app.db.db import get_session

# Importa los esquemas de Logro
from app.schemas.logro import (
    LogroCreate,
    LogroRead,
    LogroUpdate
)

# Importa los servicios relacionados con Logro
from app.services import logro as service


# Crea el router para las rutas de logros
router = APIRouter(
    prefix="/logros",   # Prefijo base de las rutas
    tags=["Logros"]     # Etiqueta para documentación Swagger
)


# Endpoint para obtener todos los logros
@router.get("/", response_model=list[LogroRead])
def get_all(
    session: Annotated[Session, Depends(get_session)]
):
    
    # Llama al servicio que obtiene todos los logros
    return service.get_all(session)


# Endpoint para obtener un logro por ID
@router.get("/{id_logro}", response_model=LogroRead)
def get_by_id(
    id_logro: UUID,
    session: Annotated[Session, Depends(get_session)]
):
    
    # Llama al servicio que busca el logro por ID
    return service.get_by_id(session, id_logro)


# Endpoint para crear un nuevo logro
@router.post("/", response_model=LogroRead, status_code=201)
def create(
    data: LogroCreate,
    session: Annotated[Session, Depends(get_session)]
):
    
    # Llama al servicio encargado de crear el logro
    return service.create(session, data)


# Endpoint para actualizar un logro existente
@router.patch("/{id_logro}", response_model=LogroRead)
def update(
    id_logro: UUID,
    data: LogroUpdate,
    session: Annotated[Session, Depends(get_session)]
):
    
    # Llama al servicio encargado de actualizar el logro
    return service.update(session, id_logro, data)


# Endpoint para eliminar un logro
@router.delete("/{id_logro}")
def delete(
    id_logro: UUID,
    session: Annotated[Session, Depends(get_session)]
):
    
    # Llama al servicio encargado de eliminar el logro
    return service.delete(session, id_logro)