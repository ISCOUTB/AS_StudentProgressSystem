
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

# Importa el esquema de respuesta del progreso
from app.schemas.progreso import ProgresoRead

# Importa los servicios relacionados con progreso académico
from app.services import progreso as service


# Crea el router para las rutas de progreso
router = APIRouter(
    prefix="/progreso",   # Prefijo base de las rutas
    tags=["Progreso"]     # Etiqueta para documentación Swagger
)


# Endpoint para obtener el progreso académico de un estudiante en una carrera
@router.get(
    "/{id_estudiante}/{id_carrera}",
    response_model=ProgresoRead
)
def get_progreso(
    id_estudiante: UUID,
    id_carrera: UUID,
    session: Annotated[Session, Depends(get_session)]
):
    
    # Llama al servicio que calcula el progreso del estudiante
    return service.get_progreso(session, id_estudiante, id_carrera)

