from sqlmodel import Session
from uuid import UUID
from app.repositories import logro_materia as repo
from app.repositories import logro as logro_repo
from app.repositories import materia as mat_repo
from app.schemas.logro_materia import LogroMateriaCreate, LogroMateriaRead
from fastapi import HTTPException

def get_all(session: Session) -> list[LogroMateriaRead]:
    return repo.get_all(session)

def get_by_logro(session: Session, id_logro: UUID) -> list[LogroMateriaRead]:
    return repo.get_by_logro(session, id_logro)

def create(session: Session, data: LogroMateriaCreate) -> LogroMateriaRead:
    logro = logro_repo.get_by_id(session, data.id_logro)
    if not logro:
        raise HTTPException(status_code=404, detail="Logro no encontrado")
    if data.id_materia:
        materia = mat_repo.get_by_id(session, data.id_materia)
        if not materia:
            raise HTTPException(status_code=404, detail="Materia no encontrada")
    return repo.create(session, data)

def delete(session: Session, id_logromateria: UUID) -> dict:
    deleted = repo.delete(session, id_logromateria)
    if not deleted:
        raise HTTPException(status_code=404, detail="LogroMateria no encontrado")
    return {"message": "LogroMateria eliminado correctamente"}