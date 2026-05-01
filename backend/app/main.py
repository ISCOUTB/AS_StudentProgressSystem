from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded
from app.db.db import create_db_and_tables
from app.core.config import settings
from app.middleware.security_headers import SecurityHeadersMiddleware
from app.middleware.rate_limit import limiter, rate_limit_exceeded_handler
from app.routes import (
    estudiante, categoria, carrera, materia,
    malla, estudiante_carrera, estudiante_materia,
    progreso, logro, logro_materia, estudiante_logro, auth
)

app = FastAPI(title=settings.APP_NAME)

# Rate limiting
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

# Security headers
app.add_middleware(SecurityHeadersMiddleware)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/")
def root():
    return {"message": "Student Progress System API running"}

app.include_router(auth.router)
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