from pydantic import Field, model_validator
from pydantic_settings import BaseSettings

# Configuración central de la aplicación cargada desde variables de entorno o .env
class Settings(BaseSettings):
    DB_USER: str = Field(default="")
    DB_PASSWORD: str = Field(default="")
    DB_HOST: str = Field(default="localhost")
    DB_PORT: int = Field(default=5432)
    DB_NAME: str = Field(default="sps_db")
    DATABASE_URL: str | None = Field(default=None)
    APP_NAME: str = Field(default="Student Progress System")
    DEBUG: bool = Field(default=False)
    # Orígenes permitidos para CORS
    ALLOWED_ORIGINS: list[str] = Field(default=[])
    # Si es True, ejecuta el seed de datos demo al iniciar
    ENABLE_DEMO_SEED: bool = Field(default=False)

    @model_validator(mode="after")
    def build_database_url(self):
        if not self.DATABASE_URL:
            self.DATABASE_URL = (
                f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@"
                f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
            )
        return self

    class Config:
        env_file = ".env"

# Instancia global de configuración usada en toda la app
settings = Settings()
