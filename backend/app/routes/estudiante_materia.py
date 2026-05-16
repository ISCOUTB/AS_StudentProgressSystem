# Importa herramientas principales de FastAPI
from fastapi import APIRouter, Depends

# Importa la sesión de SQLModel para interactuar con la base de datos
from sqlmodel import Session

# Importa Annotated para manejar dependencias tipadas
from typing import Annotated

# Importa UUID para manejar identificadores únicos
from uuid import UUID

# Importa la función que proporciona la sesión de base de datos
from app.db.db import get_session

# Importa los esquemas relacionados con estudiante-materia
from app.schemas.estudiante_materia import (
    EstudianteMateriaCreate,
    EstudianteMateriaRead,
    EstudianteMateriaUpdate
)

# Importa los servicios relacionados con estudiante-materia
from app.services import estudiante_materia as service


# Crea el router para las rutas de estudiante-materia
router = APIRouter(
    prefix="/estudiante-materia",   # Prefijo principal de las rutas
    tags=["Estudiante Materia"]     # Etiqueta usada en Swagger
)


# Endpoint para obtener las materias de un estudiante
@router.get("/{id_estudiante}", response_model=list[EstudianteMateriaRead])
def get_by_estudiante(
    id_estudiante: UUID,
    session: Annotated[Session, Depends(get_session)]
):
    
    # Llama al servicio que obtiene las materias del estudiante
    return service.get_by_estudiante(session, id_estudiante)


# Endpoint para crear una nueva relación estudiante-materia
@router.post("/", response_model=EstudianteMateriaRead, status_code=201)
def create(
    data: EstudianteMateriaCreate,
    session: Annotated[Session, Depends(get_session)]
):
    
    # Llama al servicio encargado de crear la relación
    return service.create(session, data)


# Endpoint para actualizar una relación estudiante-materia
@router.patch("/{id_estudiante}/{id_materia}", response_model=EstudianteMateriaRead)
def update(
    id_estudiante: UUID,
    id_materia: UUID,
    data: EstudianteMateriaUpdate,
    session: Annotated[Session, Depends(get_session)]
):
    
    # Llama al servicio encargado de actualizar la relación
    return service.update(
        session,
        id_estudiante,
        id_materia,
        data
    )


# Endpoint para eliminar una relación estudiante-materia
@router.delete("/{id_estudiante}/{id_materia}")
def delete(
    id_estudiante: UUID,
    id_materia: UUID,
    session: Annotated[Session, Depends(get_session)]
):
    
    # Llama al servicio encargado de eliminar la relación
    return service.delete(
        session,
        id_estudiante,
        id_materia
    )