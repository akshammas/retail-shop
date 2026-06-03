# app/core/config.py

from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    app_name: str = "Retail Shop API"
    app_version: str = "1.0.0"
    debug: bool = True
    secret_key: str
    database_url: str = "sqlite:///./test.db"
    allowed_origins: str = "http://localhost:3000"

    # convert comma separated string into a list
    @property
    def origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.allowed_origins.split(",")]

    class Config:
        env_file = ".env"


settings = Settings()