from sqlmodel import Session
from uuid import UUID
from app.repositories import carrera as repo
from app.schemas.carrera import CarreraCreate, CarreraUpdate, CarreraRead
from fastapi import HTTPException

def get_all(session: Session) -> list[CarreraRead]:
    return repo.get_all(session)

def get_by_id(session: Session, id_carrera: UUID) -> CarreraRead:
    carrera = repo.get_by_id(session, id_carrera)
    if not carrera:
        raise HTTPException(status_code=404, detail="Carrera no encontrada")
    return carrera

def create(session: Session, data: CarreraCreate) -> CarreraRead:
    existing = repo.get_by_codigo(session, data.codigo)
    if existing:
        raise HTTPException(status_code=400, detail="Ya existe una carrera con ese código")
    return repo.create(session, data)

def update(session: Session, id_carrera: UUID, data: CarreraUpdate) -> CarreraRead:
    carrera = repo.update(session, id_carrera, data)
    if not carrera:
        raise HTTPException(status_code=404, detail="Carrera no encontrada")
    return carrera

def delete(session: Session, id_carrera: UUID) -> dict:
    deleted = repo.delete(session, id_carrera)
    if not deleted:
        raise HTTPException(status_code=404, detail="Carrera no encontrada")
    return {"message": "Carrera eliminada correctamente"}