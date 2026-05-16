
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

# Importa los esquemas relacionados con la malla curricular
from app.schemas.malla import (
    MallaCreate,
    MallaRead,
    MallaCompletaRead
)

# Importa los servicios de malla
from app.services import malla as service


# Crea el router para las rutas de malla curricular
router = APIRouter(
    prefix="/malla",   # Prefijo base de las rutas
    tags=["Malla"]     # Etiqueta para documentación Swagger
)


# Endpoint para obtener la malla completa de una carrera
@router.get("/{id_carrera}", response_model=MallaCompletaRead)
def get_malla(
    id_carrera: UUID,
    session: Annotated[Session, Depends(get_session)]
):
    
    # Llama al servicio que obtiene la malla por carrera
    return service.get_malla_by_carrera(session, id_carrera)


# Endpoint para agregar una materia a la malla curricular
@router.post("/", response_model=MallaRead, status_code=201)
def add_materia(
    data: MallaCreate,
    session: Annotated[Session, Depends(get_session)]
):
    
    # Llama al servicio encargado de agregar la materia a la malla
    return service.add_materia(session, data)


# Endpoint para eliminar una materia de la malla curricular
@router.delete("/{id_carrera}/{id_materia}")
def remove_materia(
    id_carrera: UUID,
    id_materia: UUID,
    session: Annotated[Session, Depends(get_session)]
):
    
    # Llama al servicio encargado de remover la materia de la malla
    return service.remove_materia(session, id_carrera, id_materia)

