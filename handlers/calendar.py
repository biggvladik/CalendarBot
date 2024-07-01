from aiogram import types, F, Router
from factory import get_event_by_name, make_str
from db import data
from keyboards.for_calendar import get_keyboard_fab,MonthCallbackFactory
from keyboards.for_start import get_start_kb

router = Router()


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
             make_str(get_event_by_name(data.select_player_name(callback.from_user.id), callback_data.value)),parse_mode='HTML')
    await callback.answer()

@router.callback_query(F.data == "Назад")
async def send_calendar_requests(callback: types.CallbackQuery):
    await callback.message.answer(
        "Выберите действие",
        reply_markup=get_start_kb()
    )
    await callback.answer()