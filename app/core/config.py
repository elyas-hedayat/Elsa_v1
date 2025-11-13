from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class Settings(BaseSettings):
    app_name: str
    app_env: str = "development"
    redis_url: str = "redis://redis:6379"
    database_url: str = "postgresql+asyncpg://postgres:postgres@db:5432/shop_db"
    sentry_dns: str
    postgres_user: str
    postgres_password: str
    postgres_db: str
    DEBUG: bool

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
