# Cоздаем класс, наследуемый от StatesGroup, для группы состояний нашей FSM
from aiogram.fsm.state import StatesGroup, State


class AdminStates(StatesGroup):
    edit_reminder_text = State()  # Состояние редактирования памятки
    list_subjects = State()  # Состояние просмотра предметов
    adding_new_subject = State()  # Состояние сохранения нового предмета
    deleting_subject = State()  # Состояние удаления предмета
    list_homework = State()  # Состояние просмотра домашних заданий
    process_homework_for_student = State()  # работа с д/з конкретного студента
    choose_user_for_work_with_schedule = State()  # работа с расписанием студента
    choose_subject_for_new_lesson = State()
    choose_date_for_next_lesson = State()  # Состояние выбора даты следующего урока
    choose_next_lesson_time = State()  # Состояние выбора времени следующего урока
    list_lessons = State()  # Состояние просмотра расписания ученика
    deleting_lesson = State()  # Состояние удаления урока из расписания
