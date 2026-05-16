from pydantic_settings import BaseSettings
from pydantic import Field
import os

# Configuración central de la aplicación cargada desde variables de entorno o .env
class Settings(BaseSettings):
    # URL de conexión a la base de datos PostgreSQL
    DATABASE_URL: str = Field(default_factory=lambda: os.getenv("DATABASE_URL", "postgresql://localhost/sps_db"))
    APP_NAME: str = "Student Progress System"
    DEBUG: bool = False
    # Orígenes permitidos para CORS
    ALLOWED_ORIGINS: list[str] = ["http://localhost:3000"]
    # Si es True, ejecuta el seed de datos demo al iniciar
    ENABLE_DEMO_SEED: bool = False

    class Config:
        env_file = ".env"

# Instancia global de configuración usada en toda la app
settings = Settings()
