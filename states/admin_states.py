# Cоздаем класс, наследуемый от StatesGroup, для группы состояний нашей FSM
from aiogram.fsm.state import StatesGroup, State


class AdminStates(StatesGroup):
    edit_reminder_text = State()  # Состояние редактирования памятки
    list_homework = State()  # Состояние просмотра домашних заданий
    process_homework_for_student = State()  # работа с д/з конкретного студента
    choose_next_lesson_date = State()  # Состояние выбора даты следующего урока
    choose_next_lesson_time = State()  # Состояние выбора времени следующего урока
