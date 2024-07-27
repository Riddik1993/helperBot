from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from configuration.utils.filters.AdminFilter import IsAdmin
from keyboards.inline_keyboard import create_inline_kb
from lexicon.lexicon import LEXICON_RU

# Инициализируем роутер уровня модуля
router = Router()
router.message.filter(IsAdmin())


# Этот хэндлер срабатывает на команду /start
@router.message(Command('admin'))
async def process_start_command(message: Message):
    main_keyboard = create_inline_kb(1, admin_schedule='Расписание', change_reminder='Изменить памятку')
    await message.answer(text=LEXICON_RU['/admin'], reply_markup=main_keyboard)
