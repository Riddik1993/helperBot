import os
from dataclasses import dataclass


@dataclass
class TelegramApi:
    token: str
    admin_ids: list[int]


@dataclass
class Configuration:
    telegram: TelegramApi


def load_config() -> Configuration:
    token = os.environ.get("BOT_TOKEN")
    admins = os.environ.get("BOT_ADMINS").split(",")
    tg_api = TelegramApi(token, admins)
    return Configuration(telegram=tg_api)
