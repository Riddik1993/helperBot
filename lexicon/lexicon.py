import enum


class LexiconRu(enum.Enum):
    list_subjects_in_admin = "Список предметов.\nНажмите на предмет, чтобы удалить.\nЛибо нажмите добавить для " + \
                             "нового предмета"
    propose_add_subject = "Введите название нового предмета"
    settings = "Настройки"


LEXICON_RU: dict[str, str] = {
    "/start": "Привет!\n\n" "Я бот-помощник Анастасии",
    "/admin": "Привет! Я Ваш бот-помощник",
    "change_reminder": "Вот старый текст памятки.\nВведите новый текст и отправьте сообщение\n\n",
    "reminder_not_set": "Памятка пока не записана",
    "no_students": "У вас пока не учеников",
    "choose_student": "Выберите ученика",
    "choose_student_for_schedule": "Выберите ученика для просмотра расписания",
    "homework_not_found": "Последнее домашнее задание не найдено",
    "homework_success_saving": "Домашнее задание обновлено",
    "propose_to_insert_homework": "Введите новое задание для ученика",
    "choose_date_for_lesson": "Пожалуйста, выберите дату следующего занятия:",
    "choose_time_for_lesson": "Теперь укажите время урока в формате HH:MM",
    "lesson_dttm_saved": "Дата и время будущего урока сохранены",
    "new_subject_saved": "Новый предмет сохранен успешно!",
    "confirm_delete_subject": "Точно удалить предмет?\n Вместе с предметом удалятся и связанные уроки!",
    "list_subjects": "Выберите предмет",
    "subject_deleted": "Предмет успешно удален!",
    "list_schedule_for_student": "Расписание: \n\n",
    "lesson_saved_succesfully": "Урок успешно сохранен",
    "wrong_lesson_time_format": "Неверный формат времени! \n Введите время в формате HH:MM",
    "press_for_cancel": "Нажмите здесь для отмены"
}
