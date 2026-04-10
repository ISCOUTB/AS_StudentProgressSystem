from sqlmodel import Session, select
from uuid import UUID
from app.models.categorias import Categorias
from app.schemas.categoria import CategoriaCreate, CategoriaUpdate

def get_all(session: Session) -> list[Categorias]:
    return session.exec(select(Categorias)).all()

def get_by_id(session: Session, id_categoria: UUID) -> Categorias | None:
    return session.get(Categorias, id_categoria)

def get_by_nombre(session: Session, nombre: str) -> Categorias | None:
    return session.exec(
        select(Categorias).where(Categorias.nombre == nombre)
    ).first()

def create(session: Session, data: CategoriaCreate) -> Categorias:
    categoria = Categorias(
        codigo=data.codigo,
        nombre=data.nombre
    )
    session.add(categoria)
    session.commit()
    session.refresh(categoria)
    return categoria

def update(session: Session, id_categoria: UUID, data: CategoriaUpdate) -> Categorias | None:
    categoria = session.get(Categorias, id_categoria)
    if not categoria:
        return None
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(categoria, key, value)
    session.add(categoria)
    session.commit()
    session.refresh(categoria)
    return categoria

def delete(session: Session, id_categoria: UUID) -> bool:
    categoria = session.get(Categorias, id_categoria)
    if not categoria:
        return False
    session.delete(categoria)
    session.commit()
    return True