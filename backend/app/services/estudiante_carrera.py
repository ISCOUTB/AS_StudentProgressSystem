
# Importa Session para manejar la conexión con la base de datos
from sqlmodel import Session

# Importa UUID para identificadores únicos
from uuid import UUID

# Importa repositorios relacionados con estudiante-carrera y validaciones
from app.repositories import estudiante_carrera as repo
from app.repositories import estudiante as est_repo
from app.repositories import carrera as carrera_repo

# Importa esquemas de estudiante-carrera
from app.schemas.estudiante_carrera import (
    EstudianteCarreraCreate,
    EstudianteCarreraUpdate,
    EstudianteCarreraRead
)

# Importa HTTPException para manejar errores HTTP
from fastapi import HTTPException


# Obtiene todas las carreras de un estudiante
def get_by_estudiante(session: Session, id_estudiante: UUID) -> list[EstudianteCarreraRead]:

    # Valida que el estudiante exista
    est = est_repo.get_by_id(session, id_estudiante)
    if not est:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")

    # Retorna las carreras asociadas al estudiante
    return repo.get_by_estudiante(session, id_estudiante)


# Crea una nueva matrícula estudiante-carrera
def create(session: Session, data: EstudianteCarreraCreate) -> EstudianteCarreraRead:

    # Valida que el estudiante exista
    est = est_repo.get_by_id(session, data.id_estudiante)
    if not est:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")

    # Valida que la carrera exista
    carrera = carrera_repo.get_by_id(session, data.id_carrera)
    if not carrera:
        raise HTTPException(status_code=404, detail="Carrera no encontrada")

    # Verifica si ya existe la matrícula
    existing = repo.get_by_ids(session, data.id_estudiante, data.id_carrera)
    if existing:
        raise HTTPException(
            status_code=400,
            detail="El estudiante ya está matriculado en esta carrera"
        )

    # Crea la relación estudiante-carrera
    return repo.create(session, data)


# Actualiza una matrícula existente
def update(
    session: Session,
    id_estudiante: UUID,
    id_carrera: UUID,
    data: EstudianteCarreraUpdate
) -> EstudianteCarreraRead:

    # Intenta actualizar la matrícula
    est_carrera = repo.update(session, id_estudiante, id_carrera, data)

    # Si no existe, lanza error
    if not est_carrera:
        raise HTTPException(status_code=404, detail="Matrícula no encontrada")

    return est_carrera


# Elimina una matrícula estudiante-carrera
def delete(session: Session, id_estudiante: UUID, id_carrera: UUID) -> dict:

    # Intenta eliminar la matrícula
    deleted = repo.delete(session, id_estudiante, id_carrera)

    # Si no existe, lanza error
    if not deleted:
        raise HTTPException(status_code=404, detail="Matrícula no encontrada")

    # Mensaje de confirmación
    return {"message": "Matrícula eliminada correctamente"}

