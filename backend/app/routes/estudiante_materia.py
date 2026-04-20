from fastapi import APIRouter, Depends
from sqlmodel import Session
from typing import Annotated
from uuid import UUID
from app.db.db import get_session
from app.schemas.estudiante_materia import EstudianteMateriaCreate, EstudianteMateriaRead, EstudianteMateriaUpdate
from app.services import estudiante_materia as service

router = APIRouter(prefix="/estudiante-materia", tags=["Estudiante Materia"])

@router.get("/{id_estudiante}", response_model=list[EstudianteMateriaRead])
def get_by_estudiante(id_estudiante: UUID, session: Annotated[Session, Depends(get_session)]):
    return service.get_by_estudiante(session, id_estudiante)

@router.post("/", response_model=EstudianteMateriaRead, status_code=201)
def create(data: EstudianteMateriaCreate, session: Annotated[Session, Depends(get_session)]):
    return service.create(session, data)

@router.patch("/{id_estudiante}/{id_materia}", response_model=EstudianteMateriaRead)
def update(id_estudiante: UUID, id_materia: UUID, data: EstudianteMateriaUpdate, session: Annotated[Session, Depends(get_session)]):
    return service.update(session, id_estudiante, id_materia, data)

@router.delete("/{id_estudiante}/{id_materia}")
def delete(id_estudiante: UUID, id_materia: UUID, session: Annotated[Session, Depends(get_session)]):
    return service.delete(session, id_estudiante, id_materia)