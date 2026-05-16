
# Importa FastAPI para crear la aplicación principal
from fastapi import FastAPI

# Middleware para manejar CORS (Cross-Origin Resource Sharing)
from fastapi.middleware.cors import CORSMiddleware

# Middleware para limitar peticiones (rate limiting)
from slowapi.middleware import SlowAPIMiddleware

# Excepción para cuando se excede el límite de peticiones
from slowapi.errors import RateLimitExceeded

# Importa función para crear la base de datos y tablas
from app.db.db import create_db_and_tables, engine

# Importa función de seed (datos iniciales)
from app.db.seed import seed

# Configuración global del proyecto
from app.core.config import settings

# Middleware personalizado de headers de seguridad
from app.middleware.security_headers import SecurityHeadersMiddleware

# Limiter y handler de rate limit personalizado
from app.middleware.rate_limit import limiter, rate_limit_exceeded_handler

# Importa todos los routers del sistema
from app.routes import (
    estudiante, categoria, carrera, materia,
    malla, estudiante_carrera, estudiante_materia,
    progreso, logro, logro_materia, estudiante_logro, auth
)

# Inicializa la aplicación FastAPI
app = FastAPI(title=settings.APP_NAME)


# =========================
# RATE LIMITING CONFIG
# =========================

# Asigna el limiter a la aplicación
app.state.limiter = limiter

# Maneja la excepción de rate limit excedido
app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)

# Activa middleware de limitación de peticiones
app.add_middleware(SlowAPIMiddleware)


# =========================
# SECURITY HEADERS
# =========================

# Agrega headers de seguridad a todas las respuestas
app.add_middleware(SecurityHeadersMiddleware)


# =========================
# CORS CONFIGURATION
# =========================

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,  # dominios permitidos
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH", "DELETE"],  # métodos permitidos
    allow_headers=["Authorization", "Content-Type"],   # headers permitidos
)


# =========================
# STARTUP EVENT
# =========================

@app.on_event("startup")
def on_startup():
    # Crea tablas en la base de datos al iniciar el servidor
    create_db_and_tables()


# =========================
# ROUTES REGISTRATION
# =========================

# Registro de rutas del sistema
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

