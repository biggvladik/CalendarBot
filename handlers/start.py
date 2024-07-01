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
        "Нажмите на кнопку, чтобы бот отправил вам расписание",
        reply_markup=get_start_kb()
    )



# @router.message(Command("test"))
# async def start_handler(message: types.Message):
#     table = """
#     ```
#     \| Заголовок 1 \| Заголовок 2 \| Заголовок 3 \|
#     \|-------------\|-------------\|-------------\|
#     \| Ячейка 1    \| Ячейка 2    \| Ячейка 3    \|
#     \| Ячейка 4    \| Ячейка 5    \| Ячейка 6    \|
#     ```
#     """
#
#     await message.answer(text=table, parse_mode='Markdown')