from fastapi import APIRouter, Depends
from sqlmodel import Session
from typing import Annotated
from uuid import UUID
from app.db.db import get_session
from app.schemas.logro_materia import LogroMateriaCreate, LogroMateriaRead
from app.services import logro_materia as service

router = APIRouter(prefix="/logro-materia", tags=["Logro Materia"])

@router.get("/", response_model=list[LogroMateriaRead])
def get_all(session: Annotated[Session, Depends(get_session)]):
    return service.get_all(session)

@router.get("/{id_logro}", response_model=list[LogroMateriaRead])
def get_by_logro(id_logro: UUID, session: Annotated[Session, Depends(get_session)]):
    return service.get_by_logro(session, id_logro)

@router.post("/", response_model=LogroMateriaRead, status_code=201)
def create(data: LogroMateriaCreate, session: Annotated[Session, Depends(get_session)]):
    return service.create(session, data)

@router.delete("/{id_logromateria}")
def delete(id_logromateria: UUID, session: Annotated[Session, Depends(get_session)]):
    return service.delete(session, id_logromateria)