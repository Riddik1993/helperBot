from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def create_inline_keyboard(inline_btns: dict[str, str], width: int = 1) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []

    for data, text in inline_btns.items():
        buttons.append(InlineKeyboardButton(text=text, callback_data=data))

    kb_builder.row(*buttons, width=width)

    return kb_builder.as_markup()
