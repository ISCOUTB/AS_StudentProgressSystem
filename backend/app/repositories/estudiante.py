from sqlmodel import Session, select
from uuid import UUID
from app.models.estudiante import Estudiantes
from app.schemas.estudiante import EstudianteCreate, EstudianteUpdate
import hashlib

def hash_password(password: str) -> str:
    """Hashea una contraseña en texto plano con SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()

def get_all(session: Session) -> list[Estudiantes]:
    """Retorna todos los estudiantes."""
    return session.exec(select(Estudiantes)).all()

def get_by_id(session: Session, id_estudiante: UUID) -> Estudiantes | None:
    """Busca un estudiante por su UUID. Retorna None si no existe."""
    return session.get(Estudiantes, id_estudiante)

def get_by_codigo(session: Session, codigo: str) -> Estudiantes | None:
    """Busca un estudiante por código estudiantil (usado para validar duplicados)."""
    return session.exec(
        select(Estudiantes).where(Estudiantes.codigo == codigo)
    ).first()

def create(session: Session, data: EstudianteCreate) -> Estudiantes:
    """Crea un estudiante hasheando su contraseña antes de persistir."""
    estudiante = Estudiantes(
        nombre=data.nombre,
        apellido=data.apellido,
        codigo=data.codigo,
        correo=data.correo,
        status=data.status,
        hash_password=hash_password(data.password)  # Nunca se almacena la contraseña en texto plano
    )
    session.add(estudiante)
    session.commit()
    session.refresh(estudiante)
    return estudiante

def update(session: Session, id_estudiante: UUID, data: EstudianteUpdate) -> Estudiantes | None:
    """Actualiza solo los campos enviados (PATCH parcial). Retorna None si no existe."""
    estudiante = session.get(Estudiantes, id_estudiante)
    if not estudiante:
        return None
    update_data = data.model_dump(exclude_unset=True)  # Ignora campos no enviados
    for key, value in update_data.items():
        setattr(estudiante, key, value)
    session.add(estudiante)
    session.commit()
    session.refresh(estudiante)
    return estudiante

def delete(session: Session, id_estudiante: UUID) -> bool:
    """Elimina un estudiante. Retorna False si no existe."""
    estudiante = session.get(Estudiantes, id_estudiante)
    if not estudiante:
        return False
    session.delete(estudiante)
    session.commit()
    return True