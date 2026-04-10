from sqlmodel import Session, select
from uuid import UUID
from app.models.estudiante_carrera import EstudiantesCarreras
from app.schemas.estudiante_carrera import EstudianteCarreraCreate, EstudianteCarreraUpdate

def get_all(session: Session) -> list[EstudiantesCarreras]:
    return session.exec(select(EstudiantesCarreras)).all()

def get_by_estudiante(session: Session, id_estudiante: UUID) -> list[EstudiantesCarreras]:
    return session.exec(
        select(EstudiantesCarreras).where(EstudiantesCarreras.id_estudiante == id_estudiante)
    ).all()

def get_by_ids(session: Session, id_estudiante: UUID, id_carrera: UUID) -> EstudiantesCarreras | None:
    return session.exec(
        select(EstudiantesCarreras)
        .where(EstudiantesCarreras.id_estudiante == id_estudiante)
        .where(EstudiantesCarreras.id_carrera == id_carrera)
    ).first()

def create(session: Session, data: EstudianteCarreraCreate) -> EstudiantesCarreras:
    est_carrera = EstudiantesCarreras(
        id_estudiante=data.id_estudiante,
        id_carrera=data.id_carrera,
        semestre=data.semestre,
        fecha_admision=data.fecha_admision
    )
    session.add(est_carrera)
    session.commit()
    session.refresh(est_carrera)
    return est_carrera

def update(session: Session, id_estudiante: UUID, id_carrera: UUID, data: EstudianteCarreraUpdate) -> EstudiantesCarreras | None:
    est_carrera = session.exec(
        select(EstudiantesCarreras)
        .where(EstudiantesCarreras.id_estudiante == id_estudiante)
        .where(EstudiantesCarreras.id_carrera == id_carrera)
    ).first()
    if not est_carrera:
        return None
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(est_carrera, key, value)
    session.add(est_carrera)
    session.commit()
    session.refresh(est_carrera)
    return est_carrera

def delete(session: Session, id_estudiante: UUID, id_carrera: UUID) -> bool:
    est_carrera = session.exec(
        select(EstudiantesCarreras)
        .where(EstudiantesCarreras.id_estudiante == id_estudiante)
        .where(EstudiantesCarreras.id_carrera == id_carrera)
    ).first()
    if not est_carrera:
        return False
    session.delete(est_carrera)
    session.commit()
    return True