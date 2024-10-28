from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, CallbackQuery
from aiogram_calendar import SimpleCalendar
from aiogram_calendar.schemas import SimpleCalendarCallback
from sqlalchemy.ext.asyncio import AsyncSession

from database.models.lesson import Lesson
from database.models.subject import Subject
from database.services.homework_services import (
    get_last_homework_for_student,
    save_homework_for_student,
)
from database.services.lesson_services import get_all_lessons_by_user, add_new_lesson, delete_lesson_by_id
from database.services.reminder_services import get_last_reminder, save_reminder
from database.services.subject_services import get_all_subjects, save_new_subject, delete_subject
from database.services.user_services import get_all_users, get_full_user_name_by_id
from filters.AdminFilter import IsAdmin
from keyboards.AdminKeysData import AdminKeysData
from keyboards.admin_menu_keyboards import (
    get_admin_main_menu_keyboard,
    create_subjects_keyboard, create_students_keyboard, create_lessons_keyboard,
)
from keyboards.inline_keyboard import create_inline_keyboard
from lexicon.AdminKeysText import AdminKeysText
from lexicon.lexicon import LexiconRu
from states.AdminStateDataKeys import AdminStateDataKeys
from states.admin_states import AdminStates
from utils.datetime_utils import create_datetime_from_parts, check_time_str_format
from utils.formatting import make_bold

# Инициализируем роутер уровня модуля
router = Router()
router.message.filter(IsAdmin())

DELETE_SUBJECT_ID_STATE_KEY = "delete_subject_id"
STUDENT_ID_STATE_KEY = "student_id"
SUBJECT_ID_STATE_KEY = "subject_id"
NEXT_LESSON_DATE_STATE_KEY = "next_lesson_date"
NEXT_LESSON_TIME_STATE_KEY = "next_lesson_time"


@router.message(Command("admin"))
async def process_admin_command(message: Message):
    main_keyboard = get_admin_main_menu_keyboard()
    await message.answer(text=LexiconRu.admin.value, reply_markup=main_keyboard)


@router.callback_query(F.data == AdminKeysData.admin.value)
async def edit_to_main_admin_menu(query: CallbackQuery, state: FSMContext):
    main_keyboard = get_admin_main_menu_keyboard()
    await query.message.edit_text(text=LexiconRu.admin.value)
    await query.message.edit_reply_markup(reply_markup=main_keyboard)
    await state.clear()


@router.callback_query(F.data == AdminKeysData.settings.value)
async def edit_to_settings_menu(query: CallbackQuery):
    keyboard = create_inline_keyboard({AdminKeysData.change_reminder.value: AdminKeysText.change_reminder.value,
                                       AdminKeysData.list_subjects.value: AdminKeysText.list_subjects.value,
                                       AdminKeysData.admin.value: AdminKeysText.back.value})
    await query.message.edit_text(text=LexiconRu.settings.value)
    await query.message.edit_reply_markup(reply_markup=keyboard)


@router.callback_query(F.data == AdminKeysData.change_reminder.value, StateFilter(default_state))
async def process_change_reminder(
        query: CallbackQuery, state: FSMContext, session: AsyncSession
):
    current_reminder = await get_last_reminder(session)
    keyboard = create_inline_keyboard({AdminKeysData.admin.value: AdminKeysText.back.value})
    await query.message.answer(
        text=LexiconRu.change_reminder.value + current_reminder, reply_markup=keyboard
    )
    await state.set_state(AdminStates.edit_reminder_text)


@router.message(StateFilter(AdminStates.edit_reminder_text))
async def process_reminder_saving(
        message: Message, state: FSMContext, session: AsyncSession
):
    await save_reminder(session=session, text=message.text)
    await message.answer(
        text=LexiconRu.reminder_refreshed.value, reply_markup=get_admin_main_menu_keyboard()
    )
    await state.clear()


@router.callback_query(F.data == AdminKeysData.list_subjects.value)
async def list_subjects(
        query: CallbackQuery, state: FSMContext, session: AsyncSession
):
    current_subjects: list[Subject] = await get_all_subjects(session)
    keyboard = create_subjects_keyboard(current_subjects,
                                        {AdminKeysData.add_subject.value: AdminKeysText.add_subject.value,
                                         AdminKeysData.settings.value: AdminKeysText.back.value
                                         })
    await query.message.edit_text(text=LexiconRu.list_subjects_in_admin.value)
    await query.message.edit_reply_markup(
        reply_markup=keyboard
    )
    await state.clear()
    await state.set_state(AdminStates.list_subjects)


@router.callback_query(F.data == AdminKeysData.add_subject.value)
async def propose_new_subject_saving(
        query: CallbackQuery, state: FSMContext):
    keyboard = create_inline_keyboard({AdminKeysData.list_subjects.value: AdminKeysText.back.value})
    await query.message.answer(
        text=LexiconRu.propose_add_subject.value, reply_markup=keyboard)
    await state.set_state(AdminStates.adding_new_subject)


@router.message(StateFilter(AdminStates.adding_new_subject))
async def process_subject_saving(
        message: Message, state: FSMContext, session: AsyncSession
):
    keyboard = create_inline_keyboard({AdminKeysData.list_subjects.value: AdminKeysText.go_to_list_subjects.value,
                                       AdminKeysData.admin.value: AdminKeysText.main_menu.value})
    await save_new_subject(session=session, subject_name=message.text)
    await message.answer(
        text=LexiconRu.new_subject_saved.value, reply_markup=keyboard
    )
    await state.clear()


@router.callback_query(StateFilter(AdminStates.list_subjects))
async def propose_delete_subject(
        query: CallbackQuery, state: FSMContext
):
    keyboard = create_inline_keyboard({AdminKeysData.confirm_delete_subject.value: AdminKeysText.agree.value,
                                       AdminKeysData.list_subjects.value: AdminKeysText.cancel.value})
    await state.set_state(AdminStates.deleting_subject)
    await state.set_data({DELETE_SUBJECT_ID_STATE_KEY: int(query.data)})
    await query.message.answer(LexiconRu.confirm_delete_subject.value, reply_markup=keyboard)


@router.callback_query(F.data == AdminKeysData.confirm_delete_subject.value,
                       StateFilter(AdminStates.deleting_subject))
async def process_delete_subject(
        query: CallbackQuery, state: FSMContext, session: AsyncSession
):
    state_data = await state.get_data()
    subject_id = state_data[DELETE_SUBJECT_ID_STATE_KEY]
    keyboard = create_inline_keyboard({AdminKeysData.list_subjects.value: AdminKeysText.go_to_list_subjects.value,
                                       AdminKeysData.admin.value: AdminKeysText.main_menu.value})
    await delete_subject(session, subject_id)
    await state.clear()
    await query.message.answer(LexiconRu.subject_deleted.value, reply_markup=keyboard)


@router.callback_query(F.data == AdminKeysData.schedule.value)
@router.callback_query(F.data == AdminKeysData.homework.value)
async def process_user_list(
        query: CallbackQuery, state: FSMContext, session: AsyncSession
):
    if query.data == AdminKeysData.schedule.value:
        await state.set_state(AdminStates.choose_user_for_work_with_schedule)

    if query.data == AdminKeysData.homework.value:
        await state.set_state(AdminStates.list_homework)

    students = await get_all_users(session)
    if len(students) == 0:
        keyboard = create_inline_keyboard({AdminKeysData.admin.value: AdminKeysText.back.value})
        await query.message.answer(
            text=LexiconRu.no_students.value, reply_markup=keyboard
        )
    else:
        keyboard = create_students_keyboard(students, {AdminKeysData.admin.value: AdminKeysText.back.value})
        await query.message.answer(
            text=LexiconRu.choose_student.value, reply_markup=keyboard
        )


@router.callback_query(StateFilter(AdminStates.list_homework))
async def process_homework_for_student(
        query: CallbackQuery, state: FSMContext, session: AsyncSession
):
    student_id = int(query.data)
    student_full_name = await get_full_user_name_by_id(session, student_id)
    await state.set_state(AdminStates.process_homework_for_student)
    await state.set_data({"student_id": student_id, "student_name": student_full_name})
    homework_text = await get_last_homework_for_student(session, student_id)
    keyboard = create_inline_keyboard(
        {AdminKeysData.edit_student_homework.value: AdminKeysText.edit_student_homework.value,
         AdminKeysData.homework.value: AdminKeysText.back.value},
        width=2)
    await query.message.answer(text=homework_text, reply_markup=keyboard)


@router.callback_query(StateFilter(AdminStates.process_homework_for_student))
async def propose_to_edit_homework_for_student(query: CallbackQuery, state: FSMContext):
    keyboard = create_inline_keyboard({AdminKeysData.homework.value: AdminKeysText.back.value})
    state_data = await state.get_data()
    student_name = state_data["student_name"]
    answer_text = (
            LexiconRu.propose_to_insert_homework.value + " " + make_bold(student_name)
    )
    await query.message.answer(text=answer_text, reply_markup=keyboard)


@router.message(StateFilter(AdminStates.process_homework_for_student))
async def edit_homework_for_student(
        message: Message, state: FSMContext, session: AsyncSession
):
    data = await state.get_data()
    student_id = data["student_id"]
    await save_homework_for_student(session, student_id, message.text)
    await state.set_state(AdminStates.list_homework)
    keyboard = create_inline_keyboard({AdminKeysData.homework.value: AdminKeysText.go_to_students_list.value,
                                       AdminKeysData.admin.value: AdminKeysText.main_menu.value})
    await message.answer(
        text=LexiconRu.homework_success_saving.value, reply_markup=keyboard
    )


@router.callback_query(StateFilter(AdminStates.choose_user_for_work_with_schedule))
async def list_schedule_for_student(
        query: CallbackQuery, state: FSMContext, session: AsyncSession
):
    await state.clear()
    student_id = int(query.data)
    await state.set_data({STUDENT_ID_STATE_KEY: student_id})
    lessons = await get_all_lessons_by_user(session, student_id)
    lessons_txt = LexiconRu.list_schedule_for_student_admin.value

    keyboard = create_lessons_keyboard(lessons, {AdminKeysData.schedule.value: AdminKeysText.back.value,
                                                 AdminKeysData.add_lesson.value: AdminKeysText.add_lesson.value
                                                 })
    await state.set_state(AdminStates.list_lessons)
    await query.message.answer(text=lessons_txt, reply_markup=keyboard)


@router.callback_query(F.data == AdminKeysData.add_lesson.value)
async def choose_subject_for_new_lesson(query: CallbackQuery, state: FSMContext, session: AsyncSession
                                        ):
    await state.set_state(AdminStates.choose_subject_for_new_lesson)
    subjects = await get_all_subjects(session)
    keyboard = create_subjects_keyboard(subjects, {AdminKeysData.schedule.value: AdminKeysText.cancel.value})
    await query.message.answer(text=LexiconRu.choose_subject.value, reply_markup=keyboard)


@router.callback_query(StateFilter(AdminStates.list_lessons))
async def confirm_to_delete_lesson(query: CallbackQuery, state: FSMContext, session: AsyncSession):
    keyboard = create_inline_keyboard({AdminKeysData.confirm_delete_lesson.value: AdminKeysText.agree.value,
                                       AdminKeysData.schedule.value: AdminKeysText.cancel.value})
    await state.set_state(AdminStates.deleting_lesson)
    await state.set_data({AdminStateDataKeys.lesson_id.value: int(query.data)})
    await query.message.answer(LexiconRu.confirm_delete_lesson.value, reply_markup=keyboard)


@router.callback_query(StateFilter(AdminStates.deleting_lesson),
                       F.data == AdminKeysData.confirm_delete_lesson.value)
async def process_delete_lesson(query: CallbackQuery, state: FSMContext, session: AsyncSession):
    state_data = await state.get_data()
    lesson_id = state_data[AdminStateDataKeys.lesson_id.value]
    keyboard = create_inline_keyboard({AdminKeysData.schedule.value: AdminKeysText.go_to_schedule.value,
                                       AdminKeysData.admin.value: AdminKeysText.main_menu.value})
    await delete_lesson_by_id(session, lesson_id)
    await state.clear()
    await query.message.answer(LexiconRu.subject_deleted.value, reply_markup=keyboard)


@router.callback_query(StateFilter(AdminStates.choose_subject_for_new_lesson))
async def choose_date_for_new_lesson(query: CallbackQuery, state: FSMContext, session: AsyncSession
                                     ):
    await state.set_state(AdminStates.choose_date_for_next_lesson)
    subject_id = int(query.data)
    await state.update_data({SUBJECT_ID_STATE_KEY: subject_id})
    await query.message.answer(
        LexiconRu.choose_date_for_lesson.value,
        reply_markup=await SimpleCalendar(locale="ru_RU").start_calendar(),
    )
    await query.message.answer(LexiconRu.press_for_cancel.value,
                               reply_markup=create_inline_keyboard(
                                   {AdminKeysData.schedule.value: AdminKeysText.cancel.value}),
                               )

    @router.callback_query(StateFilter(AdminStates.choose_date_for_next_lesson), SimpleCalendarCallback.filter())
    async def process_lesson_date_selection(
            callback_query: CallbackQuery,
            callback_data: CallbackData,
            state: FSMContext,
            session: AsyncSession,
    ):
        calendar = SimpleCalendar(locale="ru_RU")
        selected, date = await calendar.process_selection(callback_query, callback_data)
        date_formatted = date.strftime("%d.%m.%Y")
        await state.update_data({NEXT_LESSON_DATE_STATE_KEY: date_formatted})
        if selected:
            keyboard = create_inline_keyboard({AdminKeysData.admin.value: AdminKeysText.cancel.value})
            await callback_query.message.answer(
                f'Вы выбрали {date.strftime("%d.%m.%Y")}\n '
                + LexiconRu.choose_time_for_lesson.value, reply_markup=keyboard
            )
            await state.set_state(AdminStates.choose_next_lesson_time)


@router.message(StateFilter(AdminStates.choose_next_lesson_time))
async def process_lesson_time_selection(
        message: Message, state: FSMContext, session: AsyncSession
):
    lesson_time = message.text
    if check_time_str_format(lesson_time):
        await state.update_data({NEXT_LESSON_TIME_STATE_KEY: lesson_time})
        data = await state.get_data()
        lesson_dttm = create_datetime_from_parts(data[NEXT_LESSON_DATE_STATE_KEY], data[NEXT_LESSON_TIME_STATE_KEY])
        lesson = Lesson(student_id=data["student_id"], subject_id=data["subject_id"],
                        lesson_dttm=lesson_dttm)
        keyboard = create_inline_keyboard({AdminKeysData.admin.value: AdminKeysText.main_menu.value})
        await add_new_lesson(session, lesson)
        await message.answer(text=LexiconRu.lesson_saved_succesfully.value, reply_markup=keyboard)
    else:
        keyboard = create_inline_keyboard({AdminKeysData.admin.value: AdminKeysText.cancel.value})
        await message.answer(text=LexiconRu.wrong_lesson_time_format.value, reply_markup=keyboard)
