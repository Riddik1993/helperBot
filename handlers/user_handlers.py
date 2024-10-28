from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from database.services.homework_services import get_last_homework_for_student
from database.services.lesson_services import get_all_lessons_by_user
from database.services.reminder_services import get_last_reminder

from keyboards.StudentKeysData import StudentKeysData
from keyboards.inline_keyboard import create_inline_keyboard
from keyboards.user_menu_keyboards import get_user_main_menu_keyboard
from lexicon.StudentKeysText import StudentKeysText
from lexicon.lexicon import LexiconRu
from utils.rendering import render_lessons_for_student

router = Router()


@router.message(CommandStart())
async def process_start_command(message: Message):
    main_keyboard = get_user_main_menu_keyboard()
    await message.answer(text=LexiconRu.start.value, reply_markup=main_keyboard)


@router.callback_query(F.data == StudentKeysData.main_user_menu.value)
async def edit_to_main_user_menu(query: CallbackQuery, state: FSMContext):
    main_keyboard = get_user_main_menu_keyboard()
    await query.message.edit_text(text=LexiconRu.start.value)
    await query.message.edit_reply_markup(reply_markup=main_keyboard)
    await state.clear()


@router.callback_query(F.data == StudentKeysData.show_reminder.value)
async def process_reminder_command(query: CallbackQuery, session: AsyncSession):
    last_reminder = await get_last_reminder(session)
    keyboard = create_inline_keyboard({StudentKeysData.main_user_menu.value: StudentKeysText.back.value})
    await query.message.answer(text=last_reminder, reply_markup=keyboard)


@router.callback_query(F.data == StudentKeysData.tasks.value)
async def show_last_homework(query: CallbackQuery, session: AsyncSession):
    last_homework = await get_last_homework_for_student(session, query.from_user.id)
    keyboard = create_inline_keyboard({StudentKeysData.main_user_menu.value: StudentKeysText.back.value})
    await query.message.answer(text=last_homework, reply_markup=keyboard)


@router.callback_query(F.data == StudentKeysData.student_schedule.value)
async def show_student_lessons(query: CallbackQuery, session: AsyncSession):
    student_lessons = await get_all_lessons_by_user(session, query.from_user.id)
    lessons_txt = LexiconRu.list_schedule_for_student.value + render_lessons_for_student(student_lessons)
    keyboard = create_inline_keyboard({StudentKeysData.main_user_menu.value: StudentKeysText.back.value})
    await query.message.answer(text=lessons_txt, reply_markup=keyboard)
