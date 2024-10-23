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
