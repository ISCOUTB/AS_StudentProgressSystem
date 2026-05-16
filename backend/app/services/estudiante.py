
# Importa Session para manejar la conexión con la base de datos
from sqlmodel import Session

# Importa UUID para identificadores únicos
from uuid import UUID

# Importa el repositorio de estudiantes (capa de acceso a datos)
from app.repositories import estudiante as repo

# Importa esquemas de estudiante
from app.schemas.estudiante import EstudianteCreate, EstudianteUpdate, EstudianteRead

# Importa HTTPException para manejar errores HTTP
from fastapi import HTTPException


# Mensaje estándar cuando un estudiante no existe
ESTUDIANTE_NO_ENCONTRADO = "Estudiante no encontrado"


# Obtiene todos los estudiantes
def get_all(session: Session) -> list[EstudianteRead]:
    return repo.get_all(session)


# Obtiene un estudiante por ID
def get_by_id(session: Session, id_estudiante: UUID) -> EstudianteRead:

    # Busca el estudiante en la base de datos
    estudiante = repo.get_by_id(session, id_estudiante)

    # Si no existe, lanza error 404
    if not estudiante:
        raise HTTPException(status_code=404, detail=ESTUDIANTE_NO_ENCONTRADO)

    return estudiante


# Crea un nuevo estudiante
def create(session: Session, data: EstudianteCreate) -> EstudianteRead:

    # Verifica si ya existe un estudiante con el mismo código
    existing = repo.get_by_codigo(session, data.codigo)

    # Si existe, lanza error 400
    if existing:
        raise HTTPException(
            status_code=400,
            detail="Ya existe un estudiante con ese código"
        )

    return repo.create(session, data)


# Actualiza un estudiante existente
def update(session: Session, id_estudiante: UUID, data: EstudianteUpdate) -> EstudianteRead:

    # Intenta actualizar el estudiante
    estudiante = repo.update(session, id_estudiante, data)

    # Si no existe, lanza error 404
    if not estudiante:
        raise HTTPException(status_code=404, detail=ESTUDIANTE_NO_ENCONTRADO)

    return estudiante


# Elimina un estudiante
def delete(session: Session, id_estudiante: UUID) -> dict:

    # Intenta eliminar el estudiante
    deleted = repo.delete(session, id_estudiante)

    # Si no existe, lanza error 404
    if not deleted:
        raise HTTPException(status_code=404, detail=ESTUDIANTE_NO_ENCONTRADO)

    # Mensaje de confirmación
    return {"message": "Estudiante eliminado correctamente"}

