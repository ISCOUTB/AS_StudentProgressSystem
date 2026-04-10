from sqlmodel import Session, select
from uuid import UUID
from app.models.estudiante_logro import EstudianteLogros
from app.schemas.estudiante_logro import EstudianteLogroCreate, EstudianteLogroUpdate

def get_by_estudiante(session: Session, id_estudiante: UUID) -> list[EstudianteLogros]:
    return session.exec(
        select(EstudianteLogros).where(EstudianteLogros.id_estudiante == id_estudiante)
    ).all()

def get_by_ids(session: Session, id_estudiante: UUID, id_logromateria: UUID) -> EstudianteLogros | None:
    return session.exec(
        select(EstudianteLogros)
        .where(EstudianteLogros.id_estudiante == id_estudiante)
        .where(EstudianteLogros.id_logromateria == id_logromateria)
    ).first()

def create(session: Session, data: EstudianteLogroCreate) -> EstudianteLogros:
    est_logro = EstudianteLogros(
        id_estudiante=data.id_estudiante,
        id_logromateria=data.id_logromateria,
        status=data.status
    )
    session.add(est_logro)
    session.commit()
    session.refresh(est_logro)
    return est_logro

def update(session: Session, id_estudiante: UUID, id_logromateria: UUID, data: EstudianteLogroUpdate) -> EstudianteLogros | None:
    est_logro = session.exec(
        select(EstudianteLogros)
        .where(EstudianteLogros.id_estudiante == id_estudiante)
        .where(EstudianteLogros.id_logromateria == id_logromateria)
    ).first()
    if not est_logro:
        return None
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(est_logro, key, value)
    session.add(est_logro)
    session.commit()
    session.refresh(est_logro)
    return est_logro

def delete(session: Session, id_estudiante: UUID, id_logromateria: UUID) -> bool:
    est_logro = session.exec(
        select(EstudianteLogros)
        .where(EstudianteLogros.id_estudiante == id_estudiante)
        .where(EstudianteLogros.id_logromateria == id_logromateria)
    ).first()
    if not est_logro:
        return False
    session.delete(est_logro)
    session.commit()
    return True