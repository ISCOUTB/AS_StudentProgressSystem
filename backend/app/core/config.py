from pydantic_settings import BaseSettings
from pydantic import Field
import os

class Settings(BaseSettings):
    DATABASE_URL: str = Field(default_factory=lambda: os.getenv("DATABASE_URL", "postgresql://localhost/sps_db"))
    APP_NAME: str = "Student Progress System"
    DEBUG: bool = False
    ALLOWED_ORIGINS: list[str] = ["http://localhost:3000"]

    class Config:
        env_file = ".env"

settings = Settings()