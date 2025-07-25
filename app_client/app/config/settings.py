import os
from pathlib import Path

from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


# Общая конфигурация
class GeneralConfig(BaseSettings):
    SECRET_KEY: str

    CLIENT_HOST: str
    CLIENT_PORT: int

    MANAGER_HOST: str
    MANAGER_PORT: int

    model_config = SettingsConfigDict(
        env_file=str(Path(__file__).resolve().parent / ".env"),
        env_file_encoding="utf-8",
        extra="allow",
    )

    @computed_field
    def BASE_DIR(self) -> str:
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    def __init__(self, **values):
        super().__init__(values)


settings = GeneralConfig()
