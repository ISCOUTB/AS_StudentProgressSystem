from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Student Progress System API running"}