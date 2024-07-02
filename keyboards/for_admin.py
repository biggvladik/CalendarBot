from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.state import StatesGroup, State

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


def get_admin_insert_kb():
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="Подтвердить",
        callback_data="Подтвердить")
    )

    builder.add(types.InlineKeyboardButton(
        text="Заполнить заново",
        callback_data="Заполнить заново")
    )
    builder.adjust(2)
    return builder.as_markup()










class ChooseUser(StatesGroup):
    choosing_id_ext = State()
    choosing_name = State()


class DeleteUser(StatesGroup):
    choosing_id_ext = State()
