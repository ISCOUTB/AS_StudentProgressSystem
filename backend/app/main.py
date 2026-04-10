from fastapi import FastAPI
from backend.app.db.db import create_db_and_tables
from app.routes import (
    estudiante,
    categoria,
    carrera,
    materia,
    malla,
    estudiante_carrera,
    estudiante_materia,
    progreso,
    logro,
    logro_materia,
    estudiante_logro
)
app = FastAPI(title="Student Progress System API")

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/")
def root():
    return {"message": "Student Progress System API running"}

app.include_router(estudiante.router)
app.include_router(categoria.router)
app.include_router(carrera.router)
app.include_router(materia.router)
app.include_router(malla.router)
app.include_router(estudiante_carrera.router)
app.include_router(estudiante_materia.router)
app.include_router(progreso.router)
app.include_router(logro.router)
app.include_router(logro_materia.router)
app.include_router(estudiante_logro.router)