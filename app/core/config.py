# app/core/config.py

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    postgres_user: str
    postgres_password: str
    postgres_db: str
    postgres_port: int
    database_url: str
    secret_key: str  # Add this line

    class Config:
        env_file = ".env"

# Initialize the settings
settings = Settings()
