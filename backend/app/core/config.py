from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://sps_user:sps_password@db:5432/sps_db"
    APP_NAME: str = "Student Progress System"
    DEBUG: bool = True

    class Config:
        env_file = ".env"

settings = Settings()