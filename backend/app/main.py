from fastapi import FastAPI
from app.db.database import create_db_and_tables
from app.routes import estudiante

app = FastAPI(title="Student Progress System API")

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/")
def root():
    return {"message": "Student Progress System API running"}

app.include_router(estudiante.router)