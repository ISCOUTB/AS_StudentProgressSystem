from fastapi import APIRouter, Depends
from typing import Annotated
from sqlmodel import Session
from uuid import UUID
from app.db.db import get_session
from app.schemas.estudiante_carrera import EstudianteCarreraCreate, EstudianteCarreraRead, EstudianteCarreraUpdate
from app.services import estudiante_carrera as service

router = APIRouter(prefix="/estudiante-carrera", tags=["Estudiante Carrera"])

@router.get("/{id_estudiante}", response_model=list[EstudianteCarreraRead])
def get_by_estudiante(id_estudiante: UUID, session: Annotated[Session, Depends(get_session)]):
    return service.get_by_estudiante(session, id_estudiante)

@router.post("/", response_model=EstudianteCarreraRead, status_code=201)
def create(data: EstudianteCarreraCreate, session: Annotated[Session, Depends(get_session)]):
    return service.create(session, data)

@router.patch("/{id_estudiante}/{id_carrera}", response_model=EstudianteCarreraRead)
def update(id_estudiante: UUID, id_carrera: UUID, data: EstudianteCarreraUpdate, session: Annotated[Session, Depends(get_session)]):
    return service.update(session, id_estudiante, id_carrera, data)

@router.delete("/{id_estudiante}/{id_carrera}")
def delete(id_estudiante: UUID, id_carrera: UUID, session: Annotated[Session, Depends(get_session)]):
    return service.delete(session, id_estudiante, id_carrera)