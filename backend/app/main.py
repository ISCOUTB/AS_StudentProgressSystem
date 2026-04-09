from fastapi import FastAPI
from app.routes import student
from app.db.db import create_db_and_tables

app = FastAPI(
    title="Student Progress System API",
    description="API para el seguimiento del progreso académico de estudiantes.",
    version="1.0.0",
)

@app.on_event("startup")
def on_startup() -> None:
    """Crea las tablas en PostgreSQL al iniciar la aplicación si no existen."""
    create_db_and_tables()

@app.get("/")
def root():
    return {"message": "Student Progress System API running"}

app.include_router(student.router)