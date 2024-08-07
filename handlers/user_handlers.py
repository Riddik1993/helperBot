from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from database.services.reminder_services import get_last_reminder
from keyboards.inline_keyboard import create_inline_kb
from keyboards.user_menu_keyboards import get_user_main_menu_keyboard
from lexicon.lexicon import LEXICON_RU

router = Router()


@router.message(CommandStart())
async def process_start_command(message: Message):
    main_keyboard = get_user_main_menu_keyboard()
    await message.answer(text=LEXICON_RU["/start"], reply_markup=main_keyboard)


@router.callback_query(F.data == "main_user_menu")
async def edit_to_main_user_menu(query: CallbackQuery, state: FSMContext):
    main_keyboard = get_user_main_menu_keyboard()
    await query.message.edit_text(text=LEXICON_RU["/start"])
    await query.message.edit_reply_markup(reply_markup=main_keyboard)
    await state.clear()


@router.callback_query(F.data == "show_reminder")
async def process_reminder_command(query: CallbackQuery, session: AsyncSession):
    last_reminder = await get_last_reminder(session)
    keyboard = create_inline_kb(1, main_user_menu="Назад")
    await query.message.answer(text=last_reminder, reply_markup=keyboard)
