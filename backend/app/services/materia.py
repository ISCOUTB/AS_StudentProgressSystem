from sqlmodel import Session
from uuid import UUID
from app.repositories import materia as repo
from app.repositories import categoria as cat_repo
from app.schemas.materia import MateriaCreate, MateriaUpdate, MateriaRead
from fastapi import HTTPException

MATERIA_NO_ENCONTRADA = "Materia no encontrada"
CATEGORIA_NO_ENCONTRADA = "Categoría no encontrada"

def get_all(session: Session) -> list[MateriaRead]:
    return repo.get_all(session)

def get_by_id(session: Session, id_materia: UUID) -> MateriaRead:
    materia = repo.get_by_id(session, id_materia)
    if not materia:
        raise HTTPException(status_code=404, detail=MATERIA_NO_ENCONTRADA)
    return materia

def get_by_categoria(session: Session, id_categoria: UUID) -> list[MateriaRead]:
    return repo.get_by_categoria(session, id_categoria)

def create(session: Session, data: MateriaCreate) -> MateriaRead:
    categoria = cat_repo.get_by_id(session, data.id_categoria)
    if not categoria:
        raise HTTPException(status_code=404, detail=CATEGORIA_NO_ENCONTRADA)
    existing = repo.get_by_nombre(session, data.nombre)
    if existing:
        raise HTTPException(status_code=400, detail="Ya existe una materia con ese nombre")
    return repo.create(session, data)

def update(session: Session, id_materia: UUID, data: MateriaUpdate) -> MateriaRead:
    if data.id_categoria:
        categoria = cat_repo.get_by_id(session, data.id_categoria)
        if not categoria:
            raise HTTPException(status_code=404, detail=CATEGORIA_NO_ENCONTRADA)
    materia = repo.update(session, id_materia, data)
    if not materia:
        raise HTTPException(status_code=404, detail=MATERIA_NO_ENCONTRADA)
    return materia

def delete(session: Session, id_materia: UUID) -> dict:
    deleted = repo.delete(session, id_materia)
    if not deleted:
        raise HTTPException(status_code=404, detail=MATERIA_NO_ENCONTRADA)
    return {"message": "Materia eliminada correctamente"}