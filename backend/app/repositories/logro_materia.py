from sqlmodel import Session, select
from uuid import UUID
from app.models.logro_materia import LogroMaterias
from app.schemas.logro_materia import LogroMateriaCreate

def get_all(session: Session) -> list[LogroMaterias]:
    """Retorna todas las asociaciones logro-materia."""
    return session.exec(select(LogroMaterias)).all()

def get_by_id(session: Session, id_logromateria: UUID) -> LogroMaterias | None:
    """Busca una asociación logro-materia por su UUID. Retorna None si no existe."""
    return session.get(LogroMaterias, id_logromateria)

def get_by_logro(session: Session, id_logro: UUID) -> list[LogroMaterias]:
    """Retorna todas las materias asociadas a un logro específico."""
    return session.exec(
        select(LogroMaterias).where(LogroMaterias.id_logro == id_logro)
    ).all()

def create(session: Session, data: LogroMateriaCreate) -> LogroMaterias:
    """Crea una asociación entre un logro y una materia."""
    logro_materia = LogroMaterias(
        id_logro=data.id_logro,
        id_materia=data.id_materia  # Puede ser None si el logro es global
    )
    session.add(logro_materia)
    session.commit()
    session.refresh(logro_materia)
    return logro_materia

def delete(session: Session, id_logromateria: UUID) -> bool:
    """Elimina una asociación logro-materia. Retorna False si no existe."""
    logro_materia = session.get(LogroMaterias, id_logromateria)
    if not logro_materia:
        return False
    session.delete(logro_materia)
    session.commit()
    return True