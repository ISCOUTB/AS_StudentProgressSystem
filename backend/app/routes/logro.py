from fastapi import APIRouter, Depends
from sqlmodel import Session
from uuid import UUID
from typing import Annotated
from app.db.db import get_session
from app.schemas.logro import LogroCreate, LogroRead, LogroUpdate
from app.services import logro as service

router = APIRouter(prefix="/logros", tags=["Logros"])

@router.get("/", response_model=list[LogroRead])
def get_all(session: Annotated[Session, Depends(get_session)]):
    return service.get_all(session)

@router.get("/{id_logro}", response_model=LogroRead)
def get_by_id(id_logro: UUID, session: Annotated[Session, Depends(get_session)]):
    return service.get_by_id(session, id_logro)

@router.post("/", response_model=LogroRead, status_code=201)
def create(data: LogroCreate, session: Annotated[Session, Depends(get_session)]):
    return service.create(session, data)

@router.patch("/{id_logro}", response_model=LogroRead)
def update(id_logro: UUID, data: LogroUpdate, session: Annotated[Session, Depends(get_session)]):
    return service.update(session, id_logro, data)

@router.delete("/{id_logro}")
def delete(id_logro: UUID, session: Annotated[Session, Depends(get_session)]):
    return service.delete(session, id_logro)