from sqlmodel import SQLModel, create_engine, Session
from app.core.config import settings
from typing import Generator, Any
import app.models  # importa todos los modelos para que SQLModel los registre


engine = create_engine(settings.DATABASE_URL, echo=True)

engine = create_engine(
    settings.DATABASE_URL,
    echo=False,           # True → imprime SQL generado (útil en desarrollo)
    pool_pre_ping=True,   # verifica la conexión antes de usarla
    pool_size=100,         # conexiones permanentes en el pool
    max_overflow=120,      # conexiones extra permitidas sobre pool_size
)

def create_db_and_tables() -> None:
    """Crea todas las tablas definidas en los modelos si no existen."""
    SQLModel.metadata.create_all(engine)

def get_session() -> Generator[Session, None, None]:
    """
    Inyecta una sesión de base de datos en cada request y la cierra
    automáticamente al terminar, aunque ocurra una excepción.
    """
    with Session(engine) as session:
        yield session