from sqlmodel import Session
from uuid import UUID
from app.repositories import logro as repo
from app.schemas.logro import LogroCreate, LogroUpdate, LogroRead
from fastapi import HTTPException

LOGRO_NO_ENCONTRADO = "Logro no encontrado"

def get_all(session: Session) -> list[LogroRead]:
    return repo.get_all(session)

def get_by_id(session: Session, id_logro: UUID) -> LogroRead:
    logro = repo.get_by_id(session, id_logro)
    if not logro:
        raise HTTPException(status_code=404, detail=LOGRO_NO_ENCONTRADO)
    return logro

def create(session: Session, data: LogroCreate) -> LogroRead:
    return repo.create(session, data)

def update(session: Session, id_logro: UUID, data: LogroUpdate) -> LogroRead:
    logro = repo.update(session, id_logro, data)
    if not logro:
        raise HTTPException(status_code=404, detail=LOGRO_NO_ENCONTRADO)
    return logro

def delete(session: Session, id_logro: UUID) -> dict:
    deleted = repo.delete(session, id_logro)
    if not deleted:
        raise HTTPException(status_code=404, detail=LOGRO_NO_ENCONTRADO)
    return {"message": "Logro eliminado correctamente"}