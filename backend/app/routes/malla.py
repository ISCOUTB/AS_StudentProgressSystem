from fastapi import APIRouter, Depends
from sqlmodel import Session
from typing import Annotated
from uuid import UUID
from app.db.db import get_session
from app.schemas.malla import MallaCreate, MallaRead, MallaCompletaRead
from app.services import malla as service

router = APIRouter(prefix="/malla", tags=["Malla"])

@router.get("/{id_carrera}", response_model=MallaCompletaRead)
def get_malla(id_carrera: UUID, session: Annotated[Session, Depends(get_session)]):
    return service.get_malla_by_carrera(session, id_carrera)

@router.post("/", response_model=MallaRead, status_code=201)
def add_materia(data: MallaCreate, session: Annotated[Session, Depends(get_session)]):
    return service.add_materia(session, data)

@router.delete("/{id_carrera}/{id_materia}")
def remove_materia(id_carrera: UUID, id_materia: UUID, session: Annotated[Session, Depends(get_session)]):
    return service.remove_materia(session, id_carrera, id_materia)