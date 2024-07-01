from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_admin_kb():
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="Добавить работника",
        callback_data="Добавить работника")
    )

    builder.add(types.InlineKeyboardButton(
        text="Удалить работника",
        callback_data="Удалить работника")
    )
    builder.add(types.InlineKeyboardButton(
        text="Показать всех работников",
        callback_data="Показать всех работников")
    )
    builder.button(
        text="Назад",
        callback_data="Назад"
    )
    builder.adjust(3)

    return builder.as_markup()
