# Cоздаем класс, наследуемый от StatesGroup, для группы состояний нашей FSM
from aiogram.fsm.state import StatesGroup, State


class AdminSettingsStates(StatesGroup):
    edit_reminder_text = State()  # Состояние редактирования памятки
