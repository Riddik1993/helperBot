# Cоздаем класс, наследуемый от StatesGroup, для группы состояний нашей FSM
from aiogram.fsm.state import StatesGroup, State


class AdminSettingsStates(StatesGroup):
    edit_reminder_text = State()  # Состояние редактирования памятки
    list_homework = State()  # Состояние просмотра домашних заданий
    process_homework_for_student = State()  # работа с д/з конкретного студента
    list_schedule = State()  # Состояние просмотра расписания
