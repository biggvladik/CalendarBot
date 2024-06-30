from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_start_kb():
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text=f"Расписание",
        callback_data="Расписание")
    )
    builder.add(types.InlineKeyboardButton(
        text="Админ-панель",
        callback_data="Админ-панель")
    )
    builder.add(types.InlineKeyboardButton(
        text="Настройки",
        callback_data="Настройки")
    )
    return builder.as_markup()