from fastapi import APIRouter, Depends
from sqlmodel import Session
from uuid import UUID
from app.db.db import get_session
from app.schemas.carrera import CarreraCreate, CarreraRead, CarreraUpdate
from app.services import carrera as service

router = APIRouter(prefix="/carreras", tags=["Carreras"])

@router.get("/", response_model=list[CarreraRead])
def get_all(session: Session = Depends(get_session)):
    return service.get_all(session)

@router.get("/{id_carrera}", response_model=CarreraRead)
def get_by_id(id_carrera: UUID, session: Session = Depends(get_session)):
    return service.get_by_id(session, id_carrera)

@router.post("/", response_model=CarreraRead, status_code=201)
def create(data: CarreraCreate, session: Session = Depends(get_session)):
    return service.create(session, data)

@router.patch("/{id_carrera}", response_model=CarreraRead)
def update(id_carrera: UUID, data: CarreraUpdate, session: Session = Depends(get_session)):
    return service.update(session, id_carrera, data)

@router.delete("/{id_carrera}")
def delete(id_carrera: UUID, session: Session = Depends(get_session)):
    return service.delete(session, id_carrera)