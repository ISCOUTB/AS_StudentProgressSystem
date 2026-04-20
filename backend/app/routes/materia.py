from fastapi import APIRouter, Depends
from sqlmodel import Session
from typing import Annotated
from uuid import UUID
from app.db.db import get_session
from app.schemas.materia import MateriaCreate, MateriaRead, MateriaUpdate
from app.services import materia as service

router = APIRouter(prefix="/materias", tags=["Materias"])

@router.get("/", response_model=list[MateriaRead])
def get_all(session: Annotated[Session, Depends(get_session)]):
    return service.get_all(session)

@router.get("/{id_materia}", response_model=MateriaRead)
def get_by_id(id_materia: UUID, session: Annotated[Session, Depends(get_session)]):
    return service.get_by_id(session, id_materia)

@router.get("/categoria/{id_categoria}", response_model=list[MateriaRead])
def get_by_categoria(id_categoria: UUID, session: Annotated[Session, Depends(get_session)]):
    return service.get_by_categoria(session, id_categoria)

@router.post("/", response_model=MateriaRead, status_code=201)
def create(data: MateriaCreate, session: Annotated[Session, Depends(get_session)]):
    return service.create(session, data)

@router.patch("/{id_materia}", response_model=MateriaRead)
def update(id_materia: UUID, data: MateriaUpdate, session: Annotated[Session, Depends(get_session)]):
    return service.update(session, id_materia, data)

@router.delete("/{id_materia}")
def delete(id_materia: UUID, session: Annotated[Session, Depends(get_session)]):
    return service.delete(session, id_materia)