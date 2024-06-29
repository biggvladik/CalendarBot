from aiogram import types, F, Router
from aiogram.types import Message
from aiogram.filters import Command
from factory import get_event_by_name,make_str
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
        text="Расписание",
        callback_data="Расписание")
    )
    builder.add(types.InlineKeyboardButton(
        text="Админ-панель",
        callback_data="Админ-панель")
    )
    await message.answer(
        "Нажмите на кнопку, чтобы бот отправил вам расписание",
        reply_markup=builder.as_markup()
    )
@router.callback_query(F.data == "Расписание")
async def send_random_value(callback: types.CallbackQuery):
    await callback.message.answer(make_str(get_event_by_name('Фирсов')))