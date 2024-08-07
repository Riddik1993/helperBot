from keyboards.inline_keyboard import create_inline_kb


def get_user_main_menu_keyboard():
    return create_inline_kb(
        schedule="Мое расписание",
        tasks="Мои задания",
        show_reminder="Памятка об уроке",
    )
