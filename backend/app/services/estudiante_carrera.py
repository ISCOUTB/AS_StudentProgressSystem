from sqlmodel import Session
from uuid import UUID
from app.repositories import estudiante_carrera as repo
from app.repositories import estudiante as est_repo
from app.repositories import carrera as carrera_repo
from app.schemas.estudiante_carrera import EstudianteCarreraCreate, EstudianteCarreraUpdate, EstudianteCarreraRead
from fastapi import HTTPException

def get_by_estudiante(session: Session, id_estudiante: UUID) -> list[EstudianteCarreraRead]:
    est = est_repo.get_by_id(session, id_estudiante)
    if not est:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    return repo.get_by_estudiante(session, id_estudiante)

def create(session: Session, data: EstudianteCarreraCreate) -> EstudianteCarreraRead:
    est = est_repo.get_by_id(session, data.id_estudiante)
    if not est:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    carrera = carrera_repo.get_by_id(session, data.id_carrera)
    if not carrera:
        raise HTTPException(status_code=404, detail="Carrera no encontrada")
    existing = repo.get_by_ids(session, data.id_estudiante, data.id_carrera)
    if existing:
        raise HTTPException(status_code=400, detail="El estudiante ya está matriculado en esta carrera")
    return repo.create(session, data)

def update(session: Session, id_estudiante: UUID, id_carrera: UUID, data: EstudianteCarreraUpdate) -> EstudianteCarreraRead:
    est_carrera = repo.update(session, id_estudiante, id_carrera, data)
    if not est_carrera:
        raise HTTPException(status_code=404, detail="Matrícula no encontrada")
    return est_carrera

def delete(session: Session, id_estudiante: UUID, id_carrera: UUID) -> dict:
    deleted = repo.delete(session, id_estudiante, id_carrera)
    if not deleted:
        raise HTTPException(status_code=404, detail="Matrícula no encontrada")
    return {"message": "Matrícula eliminada correctamente"}