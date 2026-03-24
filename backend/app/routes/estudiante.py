from fastapi import APIRouter, Depends
from sqlmodel import Session
from uuid import UUID
from app.db.database import get_session
from app.schemas.estudiante import EstudianteCreate, EstudianteRead, EstudianteUpdate
from app.services import estudiante as service

router = APIRouter(prefix="/estudiantes", tags=["Estudiantes"])

@router.get("/", response_model=list[EstudianteRead])
def get_all(session: Session = Depends(get_session)):
    return service.get_all(session)

@router.get("/{id_estudiante}", response_model=EstudianteRead)
def get_by_id(id_estudiante: UUID, session: Session = Depends(get_session)):
    return service.get_by_id(session, id_estudiante)

@router.post("/", response_model=EstudianteRead, status_code=201)
def create(data: EstudianteCreate, session: Session = Depends(get_session)):
    return service.create(session, data)

@router.patch("/{id_estudiante}", response_model=EstudianteRead)
def update(id_estudiante: UUID, data: EstudianteUpdate, session: Session = Depends(get_session)):
    return service.update(session, id_estudiante, data)

@router.delete("/{id_estudiante}")
def delete(id_estudiante: UUID, session: Session = Depends(get_session)):
    return service.delete(session, id_estudiante)