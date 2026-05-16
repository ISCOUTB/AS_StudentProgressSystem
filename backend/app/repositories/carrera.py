from sqlmodel import Session, select
from uuid import UUID
from app.models.carrera import Carreras
from app.schemas.carrera import CarreraCreate, CarreraUpdate

def get_all(session: Session) -> list[Carreras]:
    """Retorna todas las carreras."""
    return session.exec(select(Carreras)).all()

def get_by_id(session: Session, id_carrera: UUID) -> Carreras | None:
    """Busca una carrera por su UUID. Retorna None si no existe."""
    return session.get(Carreras, id_carrera)

def get_by_codigo(session: Session, codigo: str) -> Carreras | None:
    """Busca una carrera por su código único (usado para validar duplicados)."""
    return session.exec(
        select(Carreras).where(Carreras.codigo == codigo)
    ).first()

def create(session: Session, data: CarreraCreate) -> Carreras:
    """Crea y persiste una nueva carrera."""
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
    """Actualiza solo los campos enviados (PATCH parcial). Retorna None si no existe."""
    carrera = session.get(Carreras, id_carrera)
    if not carrera:
        return None
    update_data = data.model_dump(exclude_unset=True)  # Ignora campos no enviados
    for key, value in update_data.items():
        setattr(carrera, key, value)
    session.add(carrera)
    session.commit()
    session.refresh(carrera)
    return carrera

def delete(session: Session, id_carrera: UUID) -> bool:
    """Elimina una carrera. Retorna False si no existe."""
    carrera = session.get(Carreras, id_carrera)
    if not carrera:
        return False
    session.delete(carrera)
    session.commit()
    return True