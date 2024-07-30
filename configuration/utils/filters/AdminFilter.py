from aiogram.filters import BaseFilter
from aiogram.types import Message

from configuration.Configuration import Configuration


class IsAdmin(BaseFilter):
    async def __call__(self, message: Message, config: Configuration) -> bool:
        return message.from_user.id in config.telegram.admin_ids
