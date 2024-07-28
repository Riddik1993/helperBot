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
class Configuration:
    telegram: TelegramApi
    db: DatabaseConfig


def load_config() -> Configuration:
    token = os.environ.get("BOT_TOKEN")
    admins = os.environ.get("BOT_ADMINS").split(",")
    tg_api = TelegramApi(token, list(map(int, admins)))

    db_dsn = os.environ.get("DB_DSN")
    db_echo = os.environ.get("DB_DSN")
    db_config = DatabaseConfig(db_dsn, bool(db_echo))
    return Configuration(telegram=tg_api, db=db_config)
