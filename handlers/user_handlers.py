from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from keyboards.inline_keyboard import create_inline_kb
from lexicon.lexicon import LEXICON_RU

# Инициализируем роутер уровня модуля
router = Router()


# Этот хэндлер срабатывает на команду /start
@router.message(CommandStart())
async def process_start_command(message: Message):
    main_keyboard = create_inline_kb(1, schedule='Мое расписание', tasks='Мои задания', reminder='Памятка об уроке')
    await message.answer(text=LEXICON_RU['/start'], reply_markup=main_keyboard)
