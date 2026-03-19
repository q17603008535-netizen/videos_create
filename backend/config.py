from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    QWEN_API_KEY: str = ""
    DEEPSEEK_API_KEY: str = ""
    ADMIN_USERNAME: str = "admin"
    ADMIN_PASSWORD: str = "admin"
    SECRET_KEY: str = "secret-key-change-in-production"
    DATABASE_URL: str = "sqlite:///data/app.db"

    class Config:
        env_file = ".env"


settings = Settings()
