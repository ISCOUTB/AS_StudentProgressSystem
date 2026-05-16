```python id="q9ms7k"
# Importa herramientas principales de FastAPI
from fastapi import APIRouter, Depends

# Importa la sesión de SQLModel para interactuar con la base de datos
from sqlmodel import Session

# Importa Annotated para manejar dependencias tipadas
from typing import Annotated

# Importa UUID para manejar identificadores únicos
from uuid import UUID

# Importa la función que genera la sesión de base de datos
from app.db.db import get_session

# Importa los esquemas relacionados con estudiante-logro
from app.schemas.estudiante_logro import (
    EstudianteLogroCreate,
    EstudianteLogroRead,
    EstudianteLogroUpdate
)

# Importa los servicios relacionados con estudiante-logro
from app.services import estudiante_logro as service


# Crea el router para las rutas de estudiante-logro
router = APIRouter(
    prefix="/estudiante-logro",   # Prefijo principal de las rutas
    tags=["Estudiante Logro"]     # Etiqueta usada en Swagger
)


# Endpoint para obtener los logros de un estudiante
@router.get("/{id_estudiante}", response_model=list[EstudianteLogroRead])
def get_by_estudiante(
    id_estudiante: UUID,
    session: Annotated[Session, Depends(get_session)]
):
    
    # Llama al servicio que obtiene los logros del estudiante
    return service.get_by_estudiante(session, id_estudiante)


# Endpoint para crear una nueva relación estudiante-logro
@router.post("/", response_model=EstudianteLogroRead, status_code=201)
def create(
    data: EstudianteLogroCreate,
    session: Annotated[Session, Depends(get_session)]
):
    
    # Llama al servicio encargado de crear la relación
    return service.create(session, data)


# Endpoint para actualizar una relación estudiante-logro
@router.patch("/{id_estudiante}/{id_logromateria}", response_model=EstudianteLogroRead)
def update(
    id_estudiante: UUID,
    id_logromateria: UUID,
    data: EstudianteLogroUpdate,
    session: Annotated[Session, Depends(get_session)]
):
    
    # Llama al servicio encargado de actualizar la relación
    return service.update(
        session,
        id_estudiante,
        id_logromateria,
        data
    )


# Endpoint para eliminar una relación estudiante-logro
@router.delete("/{id_estudiante}/{id_logromateria}")
def delete(
    id_estudiante: UUID,
    id_logromateria: UUID,
    session: Annotated[Session, Depends(get_session)]
):
    
    # Llama al servicio encargado de eliminar la relación
    return service.delete(
        session,
        id_estudiante,
        id_logromateria
    )
```
