from sqlmodel import Session, select
from uuid import UUID
from app.models.carrera import Carreras
from app.schemas.carrera import CarreraCreate, CarreraUpdate

def get_all(session: Session) -> list[Carreras]:
    return session.exec(select(Carreras)).all()

def get_by_id(session: Session, id_carrera: UUID) -> Carreras | None:
    return session.get(Carreras, id_carrera)

def get_by_codigo(session: Session, codigo: str) -> Carreras | None:
    return session.exec(
        select(Carreras).where(Carreras.codigo == codigo)
    ).first()

def create(session: Session, data: CarreraCreate) -> Carreras:
    carrera = Carreras(
        nombre=data.nombre,
        codigo=data.codigo,
        escuela=data.escuela
    )
    session.add(carrera)
    session.commit()
    session.refresh(carrera)
    return carrera

def update(session: Session, id_carrera: UUID, data: CarreraUpdate) -> Carreras | None:
    carrera = session.get(Carreras, id_carrera)
    if not carrera:
        return None
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(carrera, key, value)
    session.add(carrera)
    session.commit()
    session.refresh(carrera)
    return carrera

def delete(session: Session, id_carrera: UUID) -> bool:
    carrera = session.get(Carreras, id_carrera)
    if not carrera:
        return False
    session.delete(carrera)
    session.commit()
    return True