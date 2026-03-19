from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    QWEN_API_KEY: str = ""
    DEEPSEEK_API_KEY: str = ""
    ADMIN_USERNAME: str = "admin"
    ADMIN_PASSWORD: Optional[str] = None
    SECRET_KEY: Optional[str] = None
    DATABASE_URL: str = "sqlite:///data/app.db"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
