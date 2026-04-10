from sqlmodel import Session
from uuid import UUID
from app.repositories import estudiante_logro as repo
from app.repositories import estudiante as est_repo
from app.repositories import logro_materia as logro_mat_repo
from app.schemas.estudiante_logro import EstudianteLogroCreate, EstudianteLogroUpdate, EstudianteLogroRead
from fastapi import HTTPException

def get_by_estudiante(session: Session, id_estudiante: UUID) -> list[EstudianteLogroRead]:
    est = est_repo.get_by_id(session, id_estudiante)
    if not est:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    return repo.get_by_estudiante(session, id_estudiante)

def create(session: Session, data: EstudianteLogroCreate) -> EstudianteLogroRead:
    est = est_repo.get_by_id(session, data.id_estudiante)
    if not est:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    logro_mat = logro_mat_repo.get_by_id(session, data.id_logromateria)
    if not logro_mat:
        raise HTTPException(status_code=404, detail="LogroMateria no encontrado")
    existing = repo.get_by_ids(session, data.id_estudiante, data.id_logromateria)
    if existing:
        raise HTTPException(status_code=400, detail="El estudiante ya tiene registrado este logro")
    return repo.create(session, data)

def update(session: Session, id_estudiante: UUID, id_logromateria: UUID, data: EstudianteLogroUpdate) -> EstudianteLogroRead:
    est_logro = repo.update(session, id_estudiante, id_logromateria, data)
    if not est_logro:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    return est_logro

def delete(session: Session, id_estudiante: UUID, id_logromateria: UUID) -> dict:
    deleted = repo.delete(session, id_estudiante, id_logromateria)
    if not deleted:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    return {"message": "Logro eliminado del estudiante correctamente"}