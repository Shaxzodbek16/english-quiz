from functools import cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    # API
    API_V1_STR: str = "/api/v1"
    BASE_URL: str = "http://localhost:8000/"

    # PROJECT METADATA
    PROJECT_NAME: str = "FastAPI Project"
    PROJECT_DESCRIPTION: str = "FastAPI Project Description"
    PROJECT_VERSION: str = "0.1.0"
    DEBUG: bool = False

    # POSTGRES CREDENTIALS
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: str = "5432"
    POSTGRES_DATABASE: str = "postgres"

    # WebApp
    BOT_TOKEN: str = "token"
    SUPERUSERS: str = "5006482590,6521856185"

    # JWT CREDENTIALS
    SECRET_KEY: str = "english_quiz_api_secret_key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    model_config = SettingsConfigDict(env_file=".env")

    @property
    def get_postgres_url(self):
        return f"{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DATABASE}"

    @property
    def get_superusers(self):
        return [int(user_id.strip()) for user_id in self.SUPERUSERS.split(",")]


@cache
def get_settings() -> Settings:
    return Settings()
