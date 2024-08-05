from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from configuration.utils.filters.AdminFilter import IsAdmin
from database.models.user import User
from database.services.homework_services import get_last_homework_for_student
from database.services.reminder_services import get_last_reminder, save_reminder
from database.services.user_services import get_all_users
from keyboards.admin_menu_keyboards import get_admin_main_menu_keyboard, get_students_keyboard
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
async def edit_to_main_admin_menu(query: CallbackQuery, state: FSMContext):
    main_keyboard = get_admin_main_menu_keyboard()
    await query.message.edit_text(text=LEXICON_RU["/admin"])
    await query.message.edit_reply_markup(reply_markup=main_keyboard)
    await state.clear()


@router.callback_query(F.data == "settings")
async def edit_to_settings_menu(query: CallbackQuery):
    keyboard = create_inline_kb(1, change_reminder="Изменить памятку", admin="Назад")
    await query.message.edit_reply_markup(reply_markup=keyboard)


@router.callback_query(F.data == "change_reminder", StateFilter(default_state))
async def process_change_reminder(
        query: CallbackQuery, state: FSMContext, session: AsyncSession
):
    current_reminder = await get_last_reminder(session)
    keyboard = create_inline_kb(admin="Назад")
    await query.message.answer(text=LEXICON_RU["change_reminder"] + current_reminder, reply_markup=keyboard)
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


@router.callback_query(F.data == "schedule")
@router.callback_query(F.data == "homework")
async def process_user_list(query: CallbackQuery, state: FSMContext, session: AsyncSession):
    if query.data == "schedule":
        await state.set_state(AdminSettingsStates.list_schedule)

    if query.data == "homework":
        await state.set_state(AdminSettingsStates.list_homework)

    students = await get_all_users(session)
    if len(students) == 0:
        keyboard = create_inline_kb(1, admin="Назад")
        await query.message.answer(text=LEXICON_RU["no_students"], reply_markup=keyboard)
    else:
        keyboard = get_students_keyboard(students, back_button_callback_data="admin")
        await query.message.answer(text=LEXICON_RU["choose_student"], reply_markup=keyboard)


@router.callback_query(StateFilter(AdminSettingsStates.list_homework))
async def process_homework_for_student(query: CallbackQuery, state: FSMContext, session: AsyncSession):
    homework_text = await get_last_homework_for_student(session, int(query.data))
    keyboard = create_inline_kb(1, homework="Назад")
    await query.message.answer(text=homework_text, reply_markup=keyboard)
