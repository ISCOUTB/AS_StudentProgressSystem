from fastapi import APIRouter, Depends
from sqlmodel import Session
from uuid import UUID
from app.db.db import get_session
from app.schemas.estudiante_logro import EstudianteLogroCreate, EstudianteLogroRead, EstudianteLogroUpdate
from app.services import estudiante_logro as service

router = APIRouter(prefix="/estudiante-logro", tags=["Estudiante Logro"])

@router.get("/{id_estudiante}", response_model=list[EstudianteLogroRead])
def get_by_estudiante(id_estudiante: UUID, session: Session = Depends(get_session)):
    return service.get_by_estudiante(session, id_estudiante)

@router.post("/", response_model=EstudianteLogroRead, status_code=201)
def create(data: EstudianteLogroCreate, session: Session = Depends(get_session)):
    return service.create(session, data)

@router.patch("/{id_estudiante}/{id_logromateria}", response_model=EstudianteLogroRead)
def update(id_estudiante: UUID, id_logromateria: UUID, data: EstudianteLogroUpdate, session: Session = Depends(get_session)):
    return service.update(session, id_estudiante, id_logromateria, data)

@router.delete("/{id_estudiante}/{id_logromateria}")
def delete(id_estudiante: UUID, id_logromateria: UUID, session: Session = Depends(get_session)):
    return service.delete(session, id_estudiante, id_logromateria)