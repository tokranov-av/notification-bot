__all__ = ("settings",)

import logging
from pathlib import Path
from typing import Literal
from zoneinfo import ZoneInfo

from pydantic import BaseModel
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)

BASE_DIR = Path(__file__).resolve().parent.parent

TIME_ZONE = ZoneInfo("Europe/Moscow")

LOG_FORMAT: str = (
    "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"
)


class LoggingConfig(BaseModel):
    log_level_name: Literal[
        "DEBUG",
        "INFO",
        "WARNING",
        "ERROR",
        "CRITICAL",
    ] = "INFO"
    log_format: str = LOG_FORMAT
    date_format: str = "%Y-%m-%d %H:%M:%S"

    @property
    def log_level(self) -> int:
        return logging.getLevelNamesMapping()[self.log_level_name]


class PostgresConfig(BaseModel):
    host: str = "localhost"
    port: int = 5432
    db: str = "postgres"
    user: str = "postgres"
    password: str = ""

    @property
    def database_url(self) -> str:
        user = f"{self.user}:{self.password}"
        database = f"{self.host}:{self.port}/{self.db}"

        return f"postgresql+asyncpg://{user}@{database}"


class TelegramBotConfig(BaseModel):
    token: str = ""
    admin_id: int = 0


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_file=BASE_DIR / ".env",
        env_nested_delimiter="__",
        env_prefix="NOTIFICATION_BOT__",
    )

    bot: TelegramBotConfig = TelegramBotConfig()
    logging: LoggingConfig = LoggingConfig()
    postgres: PostgresConfig = PostgresConfig()


settings = Settings()
