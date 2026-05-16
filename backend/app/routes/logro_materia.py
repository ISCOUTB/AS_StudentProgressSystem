
# Importa herramientas principales de FastAPI
from fastapi import APIRouter, Depends

# Importa la sesión de SQLModel para interactuar con la base de datos
from sqlmodel import Session

# Importa Annotated para tipado de dependencias
from typing import Annotated

# Importa UUID para manejo de identificadores únicos
from uuid import UUID

# Importa la función que genera la sesión de base de datos
from app.db.db import get_session

# Importa los esquemas de logro-materia
from app.schemas.logro_materia import (
    LogroMateriaCreate,
    LogroMateriaRead
)

# Importa los servicios relacionados con logro-materia
from app.services import logro_materia as service


# Crea el router para las rutas de logro-materia
router = APIRouter(
    prefix="/logro-materia",   # Prefijo base de las rutas
    tags=["Logro Materia"]     # Etiqueta para documentación Swagger
)


# Endpoint para obtener todos los registros de logro-materia
@router.get("/", response_model=list[LogroMateriaRead])
def get_all(
    session: Annotated[Session, Depends(get_session)]
):
    
    # Llama al servicio que obtiene todos los registros
    return service.get_all(session)


# Endpoint para obtener los logros asociados a una materia específica
@router.get("/{id_logro}", response_model=list[LogroMateriaRead])
def get_by_logro(
    id_logro: UUID,
    session: Annotated[Session, Depends(get_session)]
):
    
    # Llama al servicio que filtra por id de logro
    return service.get_by_logro(session, id_logro)


# Endpoint para crear una nueva relación logro-materia
@router.post("/", response_model=LogroMateriaRead, status_code=201)
def create(
    data: LogroMateriaCreate,
    session: Annotated[Session, Depends(get_session)]
):
    
    # Llama al servicio encargado de crear la relación
    return service.create(session, data)


# Endpoint para eliminar una relación logro-materia
@router.delete("/{id_logromateria}")
def delete(
    id_logromateria: UUID,
    session: Annotated[Session, Depends(get_session)]
):
    
    # Llama al servicio encargado de eliminar la relación
    return service.delete(session, id_logromateria)

