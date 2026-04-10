from sqlmodel import Session
from uuid import UUID
from app.repositories import malla as repo
from app.repositories import carrera as carrera_repo
from app.repositories import materia as materia_repo
from app.schemas.malla import MallaCreate, MallaRead, MallaCompletaRead
from app.schemas.materia import MateriaRead
from fastapi import HTTPException

def get_malla_by_carrera(session: Session, id_carrera: UUID) -> MallaCompletaRead:
    carrera = carrera_repo.get_by_id(session, id_carrera)
    if not carrera:
        raise HTTPException(status_code=404, detail="Carrera no encontrada")
    materias = repo.get_materias_by_carrera(session, id_carrera)
    return MallaCompletaRead(
        id_carrera=carrera.id_carrera,
        nombre=carrera.nombre,
        codigo=carrera.codigo,
        materias=[MateriaRead.model_validate(m) for m in materias]
    )

def add_materia(session: Session, data: MallaCreate) -> MallaRead:
    carrera = carrera_repo.get_by_id(session, data.id_carrera)
    if not carrera:
        raise HTTPException(status_code=404, detail="Carrera no encontrada")
    materia = materia_repo.get_by_id(session, data.id_materia)
    if not materia:
        raise HTTPException(status_code=404, detail="Materia no encontrada")
    existing = repo.get_by_ids(session, data.id_carrera, data.id_materia)
    if existing:
        raise HTTPException(status_code=400, detail="La materia ya está en la malla de esta carrera")
    return repo.create(session, data.id_carrera, data.id_materia)

def remove_materia(session: Session, id_carrera: UUID, id_materia: UUID) -> dict:
    deleted = repo.delete(session, id_carrera, id_materia)
    if not deleted:
        raise HTTPException(status_code=404, detail="Relación no encontrada en la malla")
    return {"message": "Materia eliminada de la malla correctamente"}