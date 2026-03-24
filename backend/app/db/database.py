from sqlmodel import SQLModel, create_engine, Session
from app.core.config import settings
import app.models  # importa todos los modelos para que SQLModel los registre

engine = create_engine(settings.DATABASE_URL, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session