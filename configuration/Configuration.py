import os
from dataclasses import dataclass


@dataclass
class TelegramApi:
    token: str
    admin_ids: list[int]


@dataclass
class DatabaseConfig:
    dsn: str
    echo: bool


@dataclass
class AppConfig:
    locale: str


@dataclass
class Configuration:
    telegram: TelegramApi
    db: DatabaseConfig
    app: AppConfig


def load_config() -> Configuration:
    token = os.environ.get("BOT_TOKEN")
    admins = os.environ.get("BOT_ADMINS").split(",")
    tg_api = TelegramApi(token, list(map(int, admins)))

    db_dsn = os.environ.get("DB_DSN")
    db_echo = os.environ.get("DB_ECHO")
    db_config = DatabaseConfig(db_dsn, bool(db_echo))

    locale = os.environ.get("BOT_HELPER_LOCALE", "ru_RU.utf8")
    app_config = AppConfig(locale)
    return Configuration(telegram=tg_api, db=db_config, app=app_config)
