from typing import Annotated
from fastapi import APIRouter, Depends
from sqlmodel import Session
from uuid import UUID
from app.deps import get_session
from app.schemas.categoria import CategoriaCreate, CategoriaRead, CategoriaUpdate
from app.services import categoria as service

router = APIRouter(prefix="/categorias", tags=["Categorias"])

@router.get("/", response_model=list[CategoriaRead])
def get_all(session: Annotated[Session, Depends(get_session)]):
    return service.get_all(session)

@router.get("/{id_categoria}", response_model=CategoriaRead)
def get_by_id(id_categoria: UUID, session: Annotated[Session, Depends(get_session)]):
    return service.get_by_id(session, id_categoria)

@router.post("/", response_model=CategoriaRead, status_code=201)
def create(data: CategoriaCreate, session: Annotated[Session, Depends(get_session)]):
    return service.create(session, data)

@router.patch("/{id_categoria}", response_model=CategoriaRead)
def update(id_categoria: UUID, data: CategoriaUpdate, session: Annotated[Session, Depends(get_session)]):
    return service.update(session, id_categoria, data)

@router.delete("/{id_categoria}")
def delete(id_categoria: UUID, session: Annotated[Session, Depends(get_session)]):
    return service.delete(session, id_categoria)