from sqlmodel import Session, select
from uuid import UUID
from app.models.logro import Logros
from app.schemas.logro import LogroCreate, LogroUpdate

def get_all(session: Session) -> list[Logros]:
    return session.exec(select(Logros)).all()

def get_by_id(session: Session, id_logro: UUID) -> Logros | None:
    return session.get(Logros, id_logro)

def create(session: Session, data: LogroCreate) -> Logros:
    logro = Logros(
        nombre=data.nombre,
        descripcion=data.descripcion,
        icon=data.icon
    )
    session.add(logro)
    session.commit()
    session.refresh(logro)
    return logro

def update(session: Session, id_logro: UUID, data: LogroUpdate) -> Logros | None:
    logro = session.get(Logros, id_logro)
    if not logro:
        return None
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(logro, key, value)
    session.add(logro)
    session.commit()
    session.refresh(logro)
    return logro

def delete(session: Session, id_logro: UUID) -> bool:
    logro = session.get(Logros, id_logro)
    if not logro:
        return False
    session.delete(logro)
    session.commit()
    return True