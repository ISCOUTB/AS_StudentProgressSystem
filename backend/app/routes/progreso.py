from fastapi import APIRouter, Depends
from sqlmodel import Session
from uuid import UUID
from app.db.db import get_session
from app.schemas.progreso import ProgresoRead
from app.services import progreso as service

router = APIRouter(prefix="/progreso", tags=["Progreso"])

@router.get("/{id_estudiante}/{id_carrera}", response_model=ProgresoRead)
def get_progreso(id_estudiante: UUID, id_carrera: UUID, session: Session = Depends(get_session)):
    return service.get_progreso(session, id_estudiante, id_carrera)