# Importa herramientas principales de FastAPI
from fastapi import APIRouter, Depends

# Importa la sesión de SQLModel para interactuar con la base de datos
from sqlmodel import Session

# Importa Annotated para tipado de dependencias
from typing import Annotated

# Importa UUID para manejar identificadores únicos
from uuid import UUID

# Importa la función que genera la sesión de base de datos
from app.db.db import get_session

# Importa los esquemas de Materia
from app.schemas.materia import (
    MateriaCreate,
    MateriaRead,
    MateriaUpdate
)

# Importa los servicios de materia
from app.services import materia as service


# Crea el router para las rutas de materias
router = APIRouter(
    prefix="/materias",   # Prefijo base de las rutas
    tags=["Materias"]     # Etiqueta para documentación Swagger
)


# Endpoint para obtener todas las materias
@router.get("/", response_model=list[MateriaRead])
def get_all(
    session: Annotated[Session, Depends(get_session)]
):
    
    # Llama al servicio que obtiene todas las materias
    return service.get_all(session)


# Endpoint para obtener una materia por ID
@router.get("/{id_materia}", response_model=MateriaRead)
def get_by_id(
    id_materia: UUID,
    session: Annotated[Session, Depends(get_session)]
):
    
    # Llama al servicio que busca la materia por ID
    return service.get_by_id(session, id_materia)


# Endpoint para obtener materias por categoría
@router.get("/categoria/{id_categoria}", response_model=list[MateriaRead])
def get_by_categoria(
    id_categoria: UUID,
    session: Annotated[Session, Depends(get_session)]
):
    
    # Llama al servicio que filtra materias por categoría
    return service.get_by_categoria(session, id_categoria)


# Endpoint para crear una nueva materia
@router.post("/", response_model=MateriaRead, status_code=201)
def create(
    data: MateriaCreate,
    session: Annotated[Session, Depends(get_session)]
):
    
    # Llama al servicio encargado de crear la materia
    return service.create(session, data)


# Endpoint para actualizar una materia existente
@router.patch("/{id_materia}", response_model=MateriaRead)
def update(
    id_materia: UUID,
    data: MateriaUpdate,
    session: Annotated[Session, Depends(get_session)]
):
    
    # Llama al servicio encargado de actualizar la materia
    return service.update(session, id_materia, data)


# Endpoint para eliminar una materia
@router.delete("/{id_materia}")
def delete(
    id_materia: UUID,
    session: Annotated[Session, Depends(get_session)]
):
    
    # Llama al servicio encargado de eliminar la materia
    return service.delete(session, id_materia)