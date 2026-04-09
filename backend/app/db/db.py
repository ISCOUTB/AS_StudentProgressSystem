from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlmodel import SQLModel
from typing import Generator
import os

# ─── Configuración de la URL de conexión ─────────────────────────────────────
# Se lee desde variable de entorno para no exponer credenciales en el código.
# Formato: postgresql+psycopg2://usuario:contraseña@host:puerto/nombre_db
DATABASE_URL: str = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://postgres:postgres@localhost:5432/student_progress_db",
)

# ─── Engine ───────────────────────────────────────────────────────────────────
engine = create_engine(
    DATABASE_URL,
    echo=False,           # True → imprime SQL generado (útil en desarrollo)
    pool_pre_ping=True,   # verifica la conexión antes de usarla
    pool_size=10,         # conexiones permanentes en el pool
    max_overflow=20,      # conexiones extra permitidas sobre pool_size
)

# ─── Session factory ──────────────────────────────────────────────────────────
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)


# ─── Crear tablas (se llama desde main.py al arrancar) ────────────────────────
def create_db_and_tables() -> None:
    """Crea todas las tablas definidas en los modelos si no existen."""
    SQLModel.metadata.create_all(engine)


# ─── Dependencia de sesión para FastAPI (Depends) ────────────────────────────
def get_session() -> Generator[Session, None, None]:
    """
    Inyecta una sesión de base de datos en cada request y la cierra
    automáticamente al terminar, aunque ocurra una excepción.

    Uso en una ruta:
        @router.get("/")
        def mi_ruta(db: Session = Depends(get_session)):
            ...
    """
    with SessionLocal() as session:
        yield session