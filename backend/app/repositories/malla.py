from sqlmodel import Session, select
from uuid import UUID
from app.models.carrera_materia import CarreraMateria
from app.models.materia import Materias
from app.models.carrera import Carreras

def get_materias_by_carrera(session: Session, id_carrera: UUID) -> list[Materias]:
    statement = (
        select(Materias)
        .join(CarreraMateria, CarreraMateria.id_materia == Materias.id_materia)
        .where(CarreraMateria.id_carrera == id_carrera)
    )
    return session.exec(statement).all()

def get_by_ids(session: Session, id_carrera: UUID, id_materia: UUID) -> CarreraMateria | None:
    return session.exec(
        select(CarreraMateria)
        .where(CarreraMateria.id_carrera == id_carrera)
        .where(CarreraMateria.id_materia == id_materia)
    ).first()

def create(session: Session, id_carrera: UUID, id_materia: UUID) -> CarreraMateria:
    malla = CarreraMateria(id_carrera=id_carrera, id_materia=id_materia)
    session.add(malla)
    session.commit()
    session.refresh(malla)
    return malla

def delete(session: Session, id_carrera: UUID, id_materia: UUID) -> bool:
    malla = session.exec(
        select(CarreraMateria)
        .where(CarreraMateria.id_carrera == id_carrera)
        .where(CarreraMateria.id_materia == id_materia)
    ).first()
    if not malla:
        return False
    session.delete(malla)
    session.commit()
    return True