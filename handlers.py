from aiogram import types, F, Router
from aiogram.filters import Command
from factory import get_event_by_name, make_str
from aiogram.utils.keyboard import InlineKeyboardBuilder
from db import data
from kb import get_keyboard_fab,MonthCallbackFactory
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


@router.callback_query(F.data == "Расписание")
async def send_calendar_requests(callback: types.CallbackQuery):
    await callback.message.answer(
        "Выберите месяц",
        reply_markup=get_keyboard_fab()
    )
    await callback.answer()


@router.callback_query(MonthCallbackFactory.filter())
async def callbacks_num_change_fab(
        callback: types.CallbackQuery,
        callback_data: MonthCallbackFactory):
    await callback.message.answer(
             make_str(get_event_by_name(data.select_player_name(callback.from_user.id), callback_data.value)))
    await callback.answer()

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
    await callback.answer()

