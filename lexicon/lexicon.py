import enum


class LexiconRu(enum.Enum):
    start = "Привет!\n\n" "Я бот-помощник Анастасии"
    list_subjects_in_admin = "Список предметов.\nНажмите на предмет, чтобы удалить.\nЛибо нажмите добавить для " + \
                             "нового предмета"
    propose_add_subject = "Введите название нового предмета"
    settings = "Настройки"
    admin = "Привет! Я Ваш бот-помощник"
    change_reminder = "Вот старый текст памятки.\nВведите новый текст и отправьте сообщение\n\n"
    reminder_refreshed = "Памятка обновлена!"
    new_subject_saved = "Новый предмет сохранен успешно!"
    confirm_delete_subject = "Точно удалить предмет?\n Вместе с предметом удалятся и связанные уроки!"
    confirm_delete_lesson = "Точно удалить урок?"
    subject_deleted = "Предмет успешно удален!"
    lesson_deleted = "Урок успешно удален!"
    no_students = "У вас пока не учеников"
    choose_student = "Выберите ученика"
    propose_to_insert_homework = "Введите новое задание для ученика"
    homework_success_saving = "Домашнее задание обновлено"
    list_schedule_for_student_admin = "Расписание.\nНажмите на урок, чтобы удалить его." + \
                                      "\nЛибо нажмите 'добавить' для нового урока"
    list_schedule_for_student = "Расписание"
    choose_subject = "Выберите предмет"
    choose_date_for_lesson = "Пожалуйста, выберите дату следующего занятия:"
    press_for_cancel = "Нажмите здесь для отмены"
    choose_time_for_lesson = "Теперь укажите время урока в формате HH:MM"
    lesson_saved_succesfully = "Урок успешно сохранен"
    wrong_lesson_time_format = "Неверный формат времени! \n Введите время в формате HH:MM"
    homework_not_found = "Нет заданий для ученика"
    reminder_not_set = "Памятка не задана"
