from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def create_inline_kb(width: int = 1, **kwargs: str) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []

    if kwargs:
        for button, text in kwargs.items():
            buttons.append(InlineKeyboardButton(text=text, callback_data=button))

    kb_builder.row(*buttons, width=width)

    return kb_builder.as_markup()


def create_inline_keyboard(inline_btns: dict[str, str], width: int = 1) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []

    for data, text in inline_btns.items():
        buttons.append(InlineKeyboardButton(text=text, callback_data=data))

    kb_builder.row(*buttons, width=width)

    return kb_builder.as_markup()
