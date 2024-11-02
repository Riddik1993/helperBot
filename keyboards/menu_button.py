from aiogram import Bot
from aiogram.types import BotCommand

from keyboards.StudentKeysData import StudentKeysData


async def set_main_menu(bot: Bot):
    main_menu_commands = [
        BotCommand(command=StudentKeysData.start.value,
                   description='Запустить бот')
    ]
    await bot.set_my_commands(main_menu_commands)