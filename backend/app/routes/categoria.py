# Importa Annotated para manejar dependencias con tipado
from typing import Annotated

# Importa herramientas principales de FastAPI
from fastapi import APIRouter, Depends

# Importa la sesión para interactuar con la base de datos
from sqlmodel import Session

# Importa UUID para manejar identificadores únicos
from uuid import UUID

# Importa la función que genera la sesión de base de datos
from app.db.db import get_session

# Importa los esquemas de categorías
from app.schemas.categoria import (
    CategoriaCreate,
    CategoriaRead,
    CategoriaUpdate
)

# Importa los servicios relacionados con categorías
from app.services import categoria as service


# Crea el router para las rutas de categorías
router = APIRouter(
    prefix="/categorias",   # Prefijo principal de las rutas
    tags=["Categorias"]     # Etiqueta usada en Swagger
)


# Endpoint para obtener todas las categorías
@router.get("/", response_model=list[CategoriaRead])
def get_all(
    session: Annotated[Session, Depends(get_session)]
):
    
    # Llama al servicio que obtiene todas las categorías
    return service.get_all(session)


# Endpoint para obtener una categoría por ID
@router.get("/{id_categoria}", response_model=CategoriaRead)
def get_by_id(
    id_categoria: UUID,
    session: Annotated[Session, Depends(get_session)]
):
    
    # Llama al servicio que busca la categoría por ID
    return service.get_by_id(session, id_categoria)


# Endpoint para crear una nueva categoría
@router.post("/", response_model=CategoriaRead, status_code=201)
def create(
    data: CategoriaCreate,
    session: Annotated[Session, Depends(get_session)]
):
    
    # Llama al servicio encargado de crear la categoría
    return service.create(session, data)


# Endpoint para actualizar una categoría existente
@router.patch("/{id_categoria}", response_model=CategoriaRead)
def update(
    id_categoria: UUID,
    data: CategoriaUpdate,
    session: Annotated[Session, Depends(get_session)]
):
    
    # Llama al servicio encargado de actualizar la categoría
    return service.update(session, id_categoria, data)


# Endpoint para eliminar una categoría
@router.delete("/{id_categoria}")
def delete(
    id_categoria: UUID,
    session: Annotated[Session, Depends(get_session)]
):
    
    # Llama al servicio encargado de eliminar la categoría
    return service.delete(session, id_categoria)