from aiogram import types, Router
from aiogram.filters import Command
from db import data
from keyboards.for_start import get_start_kb

router = Router()


@router.message(Command("start"))
async def start_handler(message: types.Message):
    # Проверка авторизованности
    flag = data.select_player_name(str(message.from_user.id))
    if not flag:
        await message.answer(
            "Вы не авторизованы!")
        return

    await message.answer(
        "Выберите действие",
        reply_markup=get_start_kb()
    )



