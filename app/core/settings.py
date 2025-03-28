from functools import cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # API
    API_V1_STR: str = "/api/v1"
    BASE_URL: str = "http://localhost:8000"

    # PROJECT METADATA
    PROJECT_NAME: str = "FastAPI Project"
    PROJECT_DESCRIPTION: str = "FastAPI Project Description"
    PROJECT_VERSION: str = "0.1.0"

    # POSTGRES CREDENTIALS
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: str = "5432"
    POSTGRES_DATABASE: str = "postgres"

    model_config = SettingsConfigDict(env_file=".env")

    @property
    def get_postgres_url(self):
        return f"{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DATABASE}"


@cache
def get_settings() -> Settings:
    return Settings()
