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
    builder.add(types.InlineKeyboardButton(
        text="Рассылка",
        callback_data="Рассылка")
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


def get_admin_distrb():
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="Сегодня",
        callback_data="Сегодня")
    )
    builder.add(types.InlineKeyboardButton(
        text="Завтра",
        callback_data="Завтра")
    )

    builder.add(types.InlineKeyboardButton(
        text="Выбрать дату",
        callback_data="Выбрать дату")
    )

    builder.add(types.InlineKeyboardButton(
        text="Результаты рассылки",
        callback_data="result distrib")
    )
    builder.add(types.InlineKeyboardButton(
        text="Назад",
        callback_data="cancel_distrib")
    )
    builder.adjust(3)
    return builder.as_markup()


def get_admin_reply():
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="Подтвердить",
        callback_data="reply_user")
    )
    return builder.as_markup()


def get_admin_distrb_result():
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="Сегодня",
        callback_data="today_result")
    )
    builder.add(types.InlineKeyboardButton(
        text="Завтра",
        callback_data="tommorow_result")
    )

    builder.add(types.InlineKeyboardButton(
        text="Выбрать дату",
        callback_data="choose_date_result")
    )

    builder.add(types.InlineKeyboardButton(
        text="Назад",
        callback_data="cancel_result")
    )
    builder.adjust(3)
    return builder.as_markup()


class ChooseUser(StatesGroup):
    choosing_id_ext = State()
    choosing_name = State()


class DeleteUser(StatesGroup):
    choosing_id_ext = State()


class ChooseData(StatesGroup):
    date = State()


class ChooseDataResult(StatesGroup):
    date = State()
