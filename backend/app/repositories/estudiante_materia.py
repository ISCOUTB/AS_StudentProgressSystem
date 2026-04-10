from sqlmodel import Session, select
from uuid import UUID
from app.models.estudiante_materia import EstudianteMateria
from app.schemas.estudiante_materia import EstudianteMateriaCreate, EstudianteMateriaUpdate
from app.enums.status_materia import StatusMaterias

def get_by_estudiante(session: Session, id_estudiante: UUID) -> list[EstudianteMateria]:
    return session.exec(
        select(EstudianteMateria).where(EstudianteMateria.id_estudiante == id_estudiante)
    ).all()

def get_by_ids(session: Session, id_estudiante: UUID, id_materia: UUID) -> EstudianteMateria | None:
    return session.exec(
        select(EstudianteMateria)
        .where(EstudianteMateria.id_estudiante == id_estudiante)
        .where(EstudianteMateria.id_materia == id_materia)
    ).first()

def get_aprobadas(session: Session, id_estudiante: UUID) -> list[EstudianteMateria]:
    return session.exec(
        select(EstudianteMateria)
        .where(EstudianteMateria.id_estudiante == id_estudiante)
        .where(EstudianteMateria.status == StatusMaterias.aprobada)
    ).all()

def create(session: Session, data: EstudianteMateriaCreate) -> EstudianteMateria:
    est_materia = EstudianteMateria(
        id_estudiante=data.id_estudiante,
        id_materia=data.id_materia,
        status=data.status,
        nota=data.nota,
        semestre=data.semestre
    )
    session.add(est_materia)
    session.commit()
    session.refresh(est_materia)
    return est_materia

def update(session: Session, id_estudiante: UUID, id_materia: UUID, data: EstudianteMateriaUpdate) -> EstudianteMateria | None:
    est_materia = session.exec(
        select(EstudianteMateria)
        .where(EstudianteMateria.id_estudiante == id_estudiante)
        .where(EstudianteMateria.id_materia == id_materia)
    ).first()
    if not est_materia:
        return None
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(est_materia, key, value)
    session.add(est_materia)
    session.commit()
    session.refresh(est_materia)
    return est_materia

def delete(session: Session, id_estudiante: UUID, id_materia: UUID) -> bool:
    est_materia = session.exec(
        select(EstudianteMateria)
        .where(EstudianteMateria.id_estudiante == id_estudiante)
        .where(EstudianteMateria.id_materia == id_materia)
    ).first()
    if not est_materia:
        return False
    session.delete(est_materia)
    session.commit()
    return True