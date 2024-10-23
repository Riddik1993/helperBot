from keyboards.StudentKeysData import StudentKeysData
from keyboards.inline_keyboard import create_inline_kb, create_inline_keyboard


def get_user_main_menu_keyboard():
    return create_inline_keyboard({StudentKeysData.student_schedule.value: "Мое расписание",
                                   StudentKeysData.tasks.value: "Мои задания",
                                   StudentKeysData.show_reminder.value: "Памятка об уроке"
                                   })
