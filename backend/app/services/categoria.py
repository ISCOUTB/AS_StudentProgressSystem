from sqlmodel import Session
from uuid import UUID
from app.repositories import categoria as repo
from app.schemas.categoria import CategoriaCreate, CategoriaUpdate, CategoriaRead
from fastapi import HTTPException

def get_all(session: Session) -> list[CategoriaRead]:
    return repo.get_all(session)

def get_by_id(session: Session, id_categoria: UUID) -> CategoriaRead:
    categoria = repo.get_by_id(session, id_categoria)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return categoria

def create(session: Session, data: CategoriaCreate) -> CategoriaRead:
    existing = repo.get_by_nombre(session, data.nombre)
    if existing:
        raise HTTPException(status_code=400, detail="Ya existe una categoría con ese nombre")
    return repo.create(session, data)

def update(session: Session, id_categoria: UUID, data: CategoriaUpdate) -> CategoriaRead:
    categoria = repo.update(session, id_categoria, data)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return categoria

def delete(session: Session, id_categoria: UUID) -> dict:
    deleted = repo.delete(session, id_categoria)
    if not deleted:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return {"message": "Categoría eliminada correctamente"}