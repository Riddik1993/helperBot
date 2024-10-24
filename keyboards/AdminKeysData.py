import enum


class AdminKeysData(enum.Enum):
    """
    Набор значений для передачи в callback в инлайн-кнопках
    для меню администратора
    """
    admin = "admin"
    schedule = "schedule"
    homework = "homework"
    settings = "settings"
    change_reminder = "change_reminder"
    list_subjects = "list_subjects"
    add_subject = "add_subject"
    confirm_delete_subject = "confirm_delete_subject"
