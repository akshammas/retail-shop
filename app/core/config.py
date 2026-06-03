# app/core/config.py

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Retail Shop API"
    app_version: str = "1.0.0"
    debug: bool = True
    secret_key: str
    database_url: str = "sqlite:///./test.db"
    allowed_origins: str = "http://localhost:3000"

    class Config:
        env_file = ".env"


# create one instance — import this everywhere
settings = Settings()