from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):

    env: str = "dev"
    SQLALCHEMY_DATABASE_URI: str = "sqlite:///chinook.db"
    SECRET_KEY: str = " "

    class Config:

        env_file = "./.env"


@lru_cache(maxsize=256)
def get_settings() -> Settings:
    print(f"{Settings}")
    settings = Settings()
    return settings
