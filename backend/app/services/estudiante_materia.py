from sqlmodel import Session
from uuid import UUID
from app.repositories import estudiante_materia as repo
from app.repositories import estudiante as est_repo
from app.repositories import materia as mat_repo
from app.schemas.estudiante_materia import EstudianteMateriaCreate, EstudianteMateriaUpdate, EstudianteMateriaRead
from fastapi import HTTPException

def get_by_estudiante(session: Session, id_estudiante: UUID) -> list[EstudianteMateriaRead]:
    est = est_repo.get_by_id(session, id_estudiante)
    if not est:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    return repo.get_by_estudiante(session, id_estudiante)

def create(session: Session, data: EstudianteMateriaCreate) -> EstudianteMateriaRead:
    est = est_repo.get_by_id(session, data.id_estudiante)
    if not est:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    materia = mat_repo.get_by_id(session, data.id_materia)
    if not materia:
        raise HTTPException(status_code=404, detail="Materia no encontrada")
    existing = repo.get_by_ids(session, data.id_estudiante, data.id_materia)
    if existing:
        raise HTTPException(status_code=400, detail="El estudiante ya tiene registrada esta materia")
    return repo.create(session, data)

def update(session: Session, id_estudiante: UUID, id_materia: UUID, data: EstudianteMateriaUpdate) -> EstudianteMateriaRead:
    est_materia = repo.update(session, id_estudiante, id_materia, data)
    if not est_materia:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    return est_materia

def delete(session: Session, id_estudiante: UUID, id_materia: UUID) -> dict:
    deleted = repo.delete(session, id_estudiante, id_materia)
    if not deleted:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    return {"message": "Materia eliminada del estudiante correctamente"}