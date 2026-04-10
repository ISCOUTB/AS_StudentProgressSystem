from sqlmodel import Session, select
from uuid import UUID
from app.models.materia import Materias
from app.schemas.materia import MateriaCreate, MateriaUpdate

def get_all(session: Session) -> list[Materias]:
    return session.exec(select(Materias)).all()

def get_by_id(session: Session, id_materia: UUID) -> Materias | None:
    return session.get(Materias, id_materia)

def get_by_nombre(session: Session, nombre: str) -> Materias | None:
    return session.exec(
        select(Materias).where(Materias.nombre == nombre)
    ).first()

def get_by_categoria(session: Session, id_categoria: UUID) -> list[Materias]:
    return session.exec(
        select(Materias).where(Materias.id_categoria == id_categoria)
    ).all()

def create(session: Session, data: MateriaCreate) -> Materias:
    materia = Materias(
        nombre=data.nombre,
        creditos=data.creditos,
        id_categoria=data.id_categoria
    )
    session.add(materia)
    session.commit()
    session.refresh(materia)
    return materia

def update(session: Session, id_materia: UUID, data: MateriaUpdate) -> Materias | None:
    materia = session.get(Materias, id_materia)
    if not materia:
        return None
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(materia, key, value)
    session.add(materia)
    session.commit()
    session.refresh(materia)
    return materia

def delete(session: Session, id_materia: UUID) -> bool:
    materia = session.get(Materias, id_materia)
    if not materia:
        return False
    session.delete(materia)
    session.commit()
    return True