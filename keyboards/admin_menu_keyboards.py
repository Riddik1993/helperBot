from aiogram.types import InlineKeyboardMarkup

from database.models.user import User
from keyboards.inline_keyboard import create_inline_kb

back_key_name = "Назад"


def get_admin_main_menu_keyboard():
    return create_inline_kb(
        schedule="Расписание", homework="Домашние задания", settings="Настройки"
    )


def get_students_keyboard(
    students: list[User], back_button_callback_data: str
) -> InlineKeyboardMarkup:
    student_keys = {
        str(student.telegram_id): student.first_name + " " + student.last_name
        for student in students
    }
    student_keys.update({back_button_callback_data: back_key_name})
    return create_inline_kb(**student_keys)
