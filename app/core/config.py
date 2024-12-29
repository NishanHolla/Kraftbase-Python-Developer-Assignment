from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    postgres_user: str
    postgres_password: str
    postgres_db: str
    postgres_port: int
    database_url: str

    class Config:
        env_file = ".env"

settings = Settings()

# Debug prints to verify environment variables
print(f"POSTGRES_USER: {settings.postgres_user}")
print(f"POSTGRES_PASSWORD: {settings.postgres_password}")
print(f"POSTGRES_DB: {settings.postgres_db}")
print(f"POSTGRES_PORT: {settings.postgres_port}")
print(f"DATABASE_URL: {settings.database_url}")
