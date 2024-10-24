from aiogram.types import InlineKeyboardMarkup

from database.models.subject import Subject
from database.models.user import User
from keyboards.AdminKeysData import AdminKeysData
from keyboards.inline_keyboard import create_inline_kb, create_inline_keyboard
from lexicon.AdminKeysText import AdminKeysText

back_key_name = "Назад"


def get_admin_main_menu_keyboard():
    return create_inline_keyboard({AdminKeysData.schedule.value: AdminKeysText.schedule.value,
                                   AdminKeysData.homework.value: AdminKeysText.homework.value,
                                   AdminKeysData.settings.value: AdminKeysText.settings.value})


def get_students_keyboard(
        students: list[User], back_button_callback_data: str
) -> InlineKeyboardMarkup:
    student_keys = {
        str(student.telegram_id): student.first_name + " " + student.last_name
        for student in students
    }
    student_keys.update({back_button_callback_data: back_key_name})
    return create_inline_kb(**student_keys)


def create_students_keyboard(
        students: list[User], additional_keys: dict[str, str]
) -> InlineKeyboardMarkup:
    student_keys = {
        str(student.telegram_id): student.first_name + " " + student.last_name
        for student in students
    }
    student_keys.update(additional_keys)
    return create_inline_keyboard(student_keys)


def get_subjects_keyboard(
        subjects: list[Subject], **additional_keys
) -> InlineKeyboardMarkup:
    subject_keys = {str(subject.id): subject.name for subject in subjects}
    subject_keys.update(additional_keys)
    return create_inline_kb(**subject_keys)


def create_subjects_keyboard(subjects: list[Subject], additional_keys: dict[str, str]) -> InlineKeyboardMarkup:
    subject_keys = {str(subject.id): subject.name for subject in subjects}
    subject_keys.update(additional_keys)
    return create_inline_keyboard(subject_keys)
