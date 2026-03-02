from fastapi import FastAPI
from app.routes import student

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Student Progress System API running"}

app.include_router(student.router)