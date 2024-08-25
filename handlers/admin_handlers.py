from datetime import datetime

from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, CallbackQuery
from aiogram_calendar import SimpleCalendar, get_user_locale
from aiogram_calendar.schemas import SimpleCalAct, SimpleCalendarCallback
from sqlalchemy.ext.asyncio import AsyncSession

from database.services.homework_services import (
    get_last_homework_for_student,
    save_homework_for_student,
)
from database.services.reminder_services import get_last_reminder, save_reminder
from database.services.user_services import get_all_users, get_full_user_name_by_id
from filters.AdminFilter import IsAdmin
from keyboards.admin_menu_keyboards import (
    get_admin_main_menu_keyboard,
    get_students_keyboard,
)
from keyboards.inline_keyboard import create_inline_kb
from lexicon.lexicon import LEXICON_RU
from states.admin_states import AdminSettingsStates
from utils.formatting import make_bold

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
    keyboard = create_inline_kb(change_reminder="Изменить памятку", admin="Назад")
    await query.message.edit_reply_markup(reply_markup=keyboard)


@router.callback_query(F.data == "change_reminder", StateFilter(default_state))
async def process_change_reminder(
        query: CallbackQuery, state: FSMContext, session: AsyncSession
):
    current_reminder = await get_last_reminder(session)
    keyboard = create_inline_kb(admin="Назад")
    await query.message.answer(
        text=LEXICON_RU["change_reminder"] + current_reminder, reply_markup=keyboard
    )
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
async def process_user_list(
        query: CallbackQuery, state: FSMContext, session: AsyncSession
):
    if query.data == "schedule":
        await state.set_state(AdminSettingsStates.list_schedule)

    if query.data == "homework":
        await state.set_state(AdminSettingsStates.list_homework)

    students = await get_all_users(session)
    if len(students) == 0:
        keyboard = create_inline_kb(admin="Назад")
        await query.message.answer(
            text=LEXICON_RU["no_students"], reply_markup=keyboard
        )
    else:
        keyboard = get_students_keyboard(students, back_button_callback_data="admin")
        await query.message.answer(
            text=LEXICON_RU["choose_student"], reply_markup=keyboard
        )


@router.callback_query(StateFilter(AdminSettingsStates.list_homework))
async def process_homework_for_student(
        query: CallbackQuery, state: FSMContext, session: AsyncSession
):
    student_id = int(query.data)
    student_full_name = await get_full_user_name_by_id(session, student_id)
    await state.set_state(AdminSettingsStates.process_homework_for_student)
    await state.set_data({"student_id": student_id, "student_name": student_full_name})
    homework_text = await get_last_homework_for_student(session, student_id)
    keyboard = create_inline_kb(
        2, edit_student_homework="Редактировать задание", homework="Назад"
    )
    await query.message.answer(text=homework_text, reply_markup=keyboard)


@router.callback_query(StateFilter(AdminSettingsStates.process_homework_for_student))
async def propose_to_edit_homework_for_student(query: CallbackQuery, state: FSMContext):
    keyboard = create_inline_kb(2, homework="Назад")
    state_data = await state.get_data()
    student_name = state_data["student_name"]
    answer_text = (
            LEXICON_RU["propose_to_insert_homework"] + " " + make_bold(student_name)
    )
    await query.message.answer(text=answer_text, reply_markup=keyboard)


@router.message(StateFilter(AdminSettingsStates.process_homework_for_student))
async def edit_homework_for_student(
        message: Message, state: FSMContext, session: AsyncSession
):
    data = await state.get_data()
    student_id = data["student_id"]
    await save_homework_for_student(session, student_id, message.text)
    await state.set_state(AdminSettingsStates.list_homework)
    keyboard = create_inline_kb(
        homework="Назад к списку учеников", admin="Главное меню"
    )
    await message.answer(
        text=LEXICON_RU["homework_success_saving"], reply_markup=keyboard
    )


@router.callback_query(StateFilter(AdminSettingsStates.list_schedule), SimpleCalendarCallback.filter())
async def process_schedule_selection(
        callback_query: CallbackQuery, callback_data: CallbackData, state: FSMContext, session: AsyncSession
):
    calendar = SimpleCalendar(locale="ru_RU")
    selected, date = await calendar.process_selection(callback_query, callback_data)
    if selected:
        await callback_query.message.answer(f'Вы выбрали {date.strftime("%d.%m.%Y")}')


@router.callback_query(StateFilter(AdminSettingsStates.list_schedule))
async def list_schedule_for_student(
        query: CallbackQuery, state: FSMContext, session: AsyncSession
):
    await query.message.answer(
        LEXICON_RU["choose_date_for_lesson"],
        reply_markup=await SimpleCalendar(locale="ru_RU").start_calendar(),
    )
