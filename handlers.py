from aiogram import types, F, Router
from aiogram.types import Message

from aiogram.filters import Command

import config
from factory import get_event_by_name,make_str,get_month
from aiogram.utils.keyboard import InlineKeyboardBuilder
from db import data
router = Router()






@router.message(Command("start"))
async def start_handler(message: types.Message):


    # Проверка авторизованности
    flag = data.select_player_name(str(message.from_user.id))
    if not flag:
        await message.answer(
            "Вы не авторизованы!")
        return
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
    await message.answer(
        "Нажмите на кнопку, чтобы бот отправил вам расписание",
        reply_markup=builder.as_markup()
    )
# @router.callback_query(F.data == "Расписание")
# async def send_random_value(callback: types.CallbackQuery):
#     await callback.message.answer(make_str(get_event_by_name('Фирсов')))



@router.callback_query(F.data == "Расписание")
async def send_calendar_requests(callback: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    buttons = get_month(config.directory_id)
    builder.add(types.InlineKeyboardButton(
        text=buttons[0],
        callback_data=buttons[0])
    )

    builder.add(types.InlineKeyboardButton(
        text=buttons[1],
        callback_data=buttons[1])
    )
    await callback.message.answer(
        "Выберите месяц",
        reply_markup=builder.as_markup()
    )

@router.callback_query(F.data == "06. Июнь  2024")
async def send_admin_requests(callback: types.CallbackQuery):
    print(data.select_player_name(callback.from_user.id))
    await callback.message.answer(make_str(get_event_by_name(data.select_player_name(callback.from_user.id),"06. Июнь  2024")))

@router.callback_query(F.data == "07. Июль  2024")
async def send_admin_requests(callback: types.CallbackQuery):
    print(data.select_player_name(callback.from_user.id))
    await callback.message.answer(make_str(get_event_by_name(data.select_player_name(callback.from_user.id),"07. Июль  2024")))




@router.callback_query(F.data == "Админ-панель")
async def send_admin_requests(callback: types.CallbackQuery):
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

    await callback.message.answer(
        "Выберите действие",
        reply_markup=builder.as_markup()
    )