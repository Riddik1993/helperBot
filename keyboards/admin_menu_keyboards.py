from keyboards.inline_keyboard import create_inline_kb


back = "back"


def get_admin_main_menu_keyboard():
    return create_inline_kb(
        1, admin_schedule="Расписание", my_students="Мои ученики", settings="Настройки"
    )
