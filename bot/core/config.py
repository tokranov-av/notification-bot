__all__ = (
    "TIME_ZONE",
    "settings",
)

import logging
from pathlib import Path
from typing import Literal
from zoneinfo import ZoneInfo

from pydantic import BaseModel
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
    YamlConfigSettingsSource,
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
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10

    @property
    def url(self) -> str:
        user = f"{self.user}:{self.password}"
        database = f"{self.host}:{self.port}/{self.db}"

        return f"postgresql+asyncpg://{user}@{database}"

    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }


class TelegramBotConfig(BaseModel):
    token: str = ""
    admin_id: int = 0


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False,
        yaml_file=(
            BASE_DIR / "config.default.yaml",
            BASE_DIR / "config.custom.yaml",
        ),
        yaml_config_section="notification-bot",
    )

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        """
        Define the sources and their order for loading the settings values.

        Args:
            settings_cls: The Settings class.
            init_settings: The `InitSettingsSource` instance.
            env_settings: The `EnvSettingsSource` instance.
            dotenv_settings: The `DotEnvSettingsSource` instance.
            file_secret_settings: The `SecretsSettingsSource` instance.

        Returns:
            A tuple containing the sources
            and their order for loading the settings values.
        """
        return (
            init_settings,
            env_settings,
            dotenv_settings,
            file_secret_settings,
            YamlConfigSettingsSource(settings_cls),
        )

    bot: TelegramBotConfig = TelegramBotConfig()
    logging: LoggingConfig = LoggingConfig()
    postgres: PostgresConfig = PostgresConfig()


settings = Settings()
