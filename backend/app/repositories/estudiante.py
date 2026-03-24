from sqlmodel import Session, select
from uuid import UUID
from app.models.estudiante import Estudiantes
from app.schemas.estudiante import EstudianteCreate, EstudianteUpdate
import hashlib

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def get_all(session: Session) -> list[Estudiantes]:
    return session.exec(select(Estudiantes)).all()

def get_by_id(session: Session, id_estudiante: UUID) -> Estudiantes | None:
    return session.get(Estudiantes, id_estudiante)

def get_by_codigo(session: Session, codigo: str) -> Estudiantes | None:
    return session.exec(
        select(Estudiantes).where(Estudiantes.codigo == codigo)
    ).first()

def create(session: Session, data: EstudianteCreate) -> Estudiantes:
    estudiante = Estudiantes(
        nombre=data.nombre,
        apellido=data.apellido,
        codigo=data.codigo,
        correo=data.correo,
        status=data.status,
        hash_password=hash_password(data.password)
    )
    session.add(estudiante)
    session.commit()
    session.refresh(estudiante)
    return estudiante

def update(session: Session, id_estudiante: UUID, data: EstudianteUpdate) -> Estudiantes | None:
    estudiante = session.get(Estudiantes, id_estudiante)
    if not estudiante:
        return None
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(estudiante, key, value)
    session.add(estudiante)
    session.commit()
    session.refresh(estudiante)
    return estudiante

def delete(session: Session, id_estudiante: UUID) -> bool:
    estudiante = session.get(Estudiantes, id_estudiante)
    if not estudiante:
        return False
    session.delete(estudiante)
    session.commit()
    return True