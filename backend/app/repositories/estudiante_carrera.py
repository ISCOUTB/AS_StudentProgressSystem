from sqlmodel import Session, select
from uuid import UUID
from app.models.estudiante_carrera import EstudiantesCarreras
from app.schemas.estudiante_carrera import EstudianteCarreraCreate, EstudianteCarreraUpdate

def get_all(session: Session) -> list[EstudiantesCarreras]:
    """Retorna todas las matrículas registradas."""
    return session.exec(select(EstudiantesCarreras)).all()

def get_by_estudiante(session: Session, id_estudiante: UUID) -> list[EstudiantesCarreras]:
    """Retorna todas las carreras en las que está matriculado un estudiante."""
    return session.exec(
        select(EstudiantesCarreras).where(EstudiantesCarreras.id_estudiante == id_estudiante)
    ).all()

def get_by_ids(session: Session, id_estudiante: UUID, id_carrera: UUID) -> EstudiantesCarreras | None:
    """Busca una matrícula por la combinación estudiante + carrera (usado para validar duplicados)."""
    return session.exec(
        select(EstudiantesCarreras)
        .where(EstudiantesCarreras.id_estudiante == id_estudiante)
        .where(EstudiantesCarreras.id_carrera == id_carrera)
    ).first()

def create(session: Session, data: EstudianteCarreraCreate) -> EstudiantesCarreras:
    """Registra la matrícula de un estudiante en una carrera."""
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
    """Actualiza solo los campos enviados (PATCH parcial). Retorna None si no existe."""
    est_carrera = session.exec(
        select(EstudiantesCarreras)
        .where(EstudiantesCarreras.id_estudiante == id_estudiante)
        .where(EstudiantesCarreras.id_carrera == id_carrera)
    ).first()
    if not est_carrera:
        return None
    update_data = data.model_dump(exclude_unset=True)  # Ignora campos no enviados
    for key, value in update_data.items():
        setattr(est_carrera, key, value)
    session.add(est_carrera)
    session.commit()
    session.refresh(est_carrera)
    return est_carrera

def delete(session: Session, id_estudiante: UUID, id_carrera: UUID) -> bool:
    """Elimina una matrícula por la combinación estudiante + carrera. Retorna False si no existe."""
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