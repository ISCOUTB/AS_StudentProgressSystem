from sqlmodel import Session
from uuid import UUID
from app.repositories import estudiante as repo
from app.schemas.estudiante import EstudianteCreate, EstudianteUpdate, EstudianteRead
from fastapi import HTTPException

ESTUDIANTE_NO_ENCONTRADO = "Estudiante no encontrado"

def get_all(session: Session) -> list[EstudianteRead]:
    return repo.get_all(session)

def get_by_id(session: Session, id_estudiante: UUID) -> EstudianteRead:
    estudiante = repo.get_by_id(session, id_estudiante)
    if not estudiante:
        raise HTTPException(status_code=404, detail=ESTUDIANTE_NO_ENCONTRADO)
    return estudiante

def create(session: Session, data: EstudianteCreate) -> EstudianteRead:
    existing = repo.get_by_codigo(session, data.codigo)
    if existing:
        raise HTTPException(status_code=400, detail="Ya existe un estudiante con ese código")
    return repo.create(session, data)

def update(session: Session, id_estudiante: UUID, data: EstudianteUpdate) -> EstudianteRead:
    estudiante = repo.update(session, id_estudiante, data)
    if not estudiante:
        raise HTTPException(status_code=404, detail=ESTUDIANTE_NO_ENCONTRADO)
    return estudiante

def delete(session: Session, id_estudiante: UUID) -> dict:
    deleted = repo.delete(session, id_estudiante)
    if not deleted:
        raise HTTPException(status_code=404, detail=ESTUDIANTE_NO_ENCONTRADO)
    return {"message": "Estudiante eliminado correctamente"}