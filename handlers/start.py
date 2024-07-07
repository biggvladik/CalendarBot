from aiogram import types, Router
from aiogram.filters import Command
from keyboards.for_start import get_start_kb
from keyboards.for_admin import  get_admin_reply
from db import data
import datetime
from factory import get_event_by_name, make_str, make_distrib
from config import bot




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

@router.message(Command("show_id"))
async def start_handler(message: types.Message):
    print(f'Ваш ID: {message.from_user.id}')
    await message.answer(f'Ваш ID: {message.from_user.id}')


@router.message(Command("send_push"))
async def send_push(message: types.Message):
    today = datetime.datetime.now() + datetime.timedelta(days=1)
    today = today.strftime('%d.%m.%Y')
    all_players = data.select_all_players_new()
    events = get_event_by_name(today)
    res = make_distrib(all_players, events)
    res_s = ''
    for event in res:
        if not event['event']:
            continue
        try:
            if make_str(event['event']) == 'Расписание не найдено!':
                continue
            await bot.send_message(int(event['id']), make_str(event['event']), parse_mode='HTML',
                                   reply_markup=get_admin_reply())
            data.insert_message_logs(today, event)
            res_s += make_str(event['event'])
        except:
            pass
    if res_s:
        await message.answer(
            res_s,
            parse_mode='HTML'
        )
    else:
        await message.answer(
            'Ничего отправлено не было!',
            parse_mode='HTML'
        )
