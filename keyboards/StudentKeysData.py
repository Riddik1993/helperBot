import enum


class StudentKeysData(enum.Enum):
    """
    Набор значений для передачи в callback в инлайн-кнопках
    для меню студента
    """
    main_user_menu = "main_user_menu"
    student_schedule = "student_schedule"
    tasks = "tasks"
    show_reminder = "show_reminder"
    start = "/start"
