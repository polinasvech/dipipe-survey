import os
from pathlib import Path

from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


# Общая конфигурация
class GeneralConfig(BaseSettings):

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int

    model_config = SettingsConfigDict(
        env_file=str(Path(__file__).resolve().parent / ".env"),
        env_file_encoding="utf-8",
        extra="allow",
    )

    @property
    def DB_DSN_SYNCH(self) -> str:
        return (
            f"postgresql+asyncpg://"
            f"f{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    @property
    def DB_DSN_ASYNCH(self) -> str:
        return (
            f"postgresql://"
            f"f{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    @computed_field
    def BASE_DIR(self) -> str:
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    def __init__(self, **values):
        super().__init__(values)
