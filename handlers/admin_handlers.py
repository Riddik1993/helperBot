from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from configuration.utils.filters.AdminFilter import IsAdmin
from database.services import save_reminder, get_last_reminder
from keyboards.admin_menu_keyboards import get_admin_main_menu_keyboard
from keyboards.inline_keyboard import create_inline_kb
from lexicon.lexicon import LEXICON_RU
from states.admin_states import AdminSettingsStates

# Инициализируем роутер уровня модуля
router = Router()
router.message.filter(IsAdmin())


@router.message(Command("admin"))
async def process_admin_command(message: Message):
    main_keyboard = get_admin_main_menu_keyboard()
    await message.answer(text=LEXICON_RU["/admin"], reply_markup=main_keyboard)


@router.callback_query(F.data == "admin")
async def edit_to_main_admin_menu(query: CallbackQuery):
    main_keyboard = get_admin_main_menu_keyboard()
    await query.message.edit_reply_markup(reply_markup=main_keyboard)


@router.callback_query(F.data == "settings")
async def edit_to_settings_menu(query: CallbackQuery):
    keyboard = create_inline_kb(1, change_reminder="Изменить памятку", admin="Назад")
    await query.message.edit_reply_markup(reply_markup=keyboard)


@router.callback_query(F.data == "change_reminder", StateFilter(default_state))
async def process_change_reminder(
    query: CallbackQuery, state: FSMContext, session: AsyncSession
):
    current_reminder = await get_last_reminder(session)
    await query.message.answer(text=LEXICON_RU["change_reminder"] + current_reminder)
    await state.set_state(AdminSettingsStates.edit_reminder_text)


@router.message(StateFilter(AdminSettingsStates.edit_reminder_text))
async def process_reminder_saving(
    message: Message, state: FSMContext, session: AsyncSession
):
    await save_reminder(session=session, text=message.text)
    await message.answer(
        text="Памятка обновлена!", reply_markup=get_admin_main_menu_keyboard()
    )
    await state.clear()
