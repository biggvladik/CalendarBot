from aiogram import types, Router
from aiogram.filters import Command

import config
from keyboards.for_start import get_start_kb
from keyboards.for_admin import get_admin_reply, get_admin_distrb_result
import datetime
from factory import get_event_by_name, make_distrib, make_result_distrib, make_full_str, get_month_full
from config import bot
from aiogram.utils.keyboard import InlineKeyboardBuilder
from db.orm_query import *
from sqlalchemy.ext.asyncio import AsyncSession

router = Router()


@router.message(Command("start"))
async def start_handler(message: types.Message, session: AsyncSession):
    # Проверка авторизованности
    flag = await select_user_name(session, str(message.from_user.id))
    if not flag:
        await message.answer(
            "Вы не авторизованы!")
        return

    await message.answer(
        "Выберите действие",
        reply_markup=get_start_kb()
    )


@router.message(Command("show_id"))
async def show_id_handler(message: types.Message):
    print(f'Ваш ID: {message.from_user.id}')
    await message.answer(f'Ваш ID: {message.from_user.id}')


@router.message(Command("send_push"))
async def send_push_handler(message: types.Message, session: AsyncSession):
    today = datetime.datetime.now() + datetime.timedelta(days=1)
    today = today.strftime('%d.%m.%Y')
    all_players = await select_all_users_new(session)
    events = get_event_by_name(today)
    res = make_distrib(all_players, events)
    flag = await check_admin_user(session, message.from_user.id)
    if not flag:
        await message.answer(
            'У вас нет админ прав!',
            parse_mode='HTML'
        )
        return

    res_s = ''
    res_false = ''
    send_events = []
    for event in res:
        if not event['event']:
            continue
        try:
            if make_str(event['event']) == 'Расписание не найдено!':
                continue
            user_name = await select_user_name_by_id(session, str(event['id']))
            await bot.send_message(int(event['id']), make_str(event['event']), parse_mode='HTML',
                                   reply_markup=get_admin_reply())
            await insert_message_logs(session, today, event)
            res_s += f'Отправлено: {user_name}\n' + make_str(event['event'])
            send_events += (event['event'])
        except Exception as error:
            print(error)
    await message.answer(
        make_full_str('✅ Отправленные события:\n' + res_s),
        parse_mode='HTML'
    )
    for event in events:
        if event not in send_events:
            res_false += make_str([event])

    await message.answer(
        make_full_str('❌ Неотправленные события:\n' + res_false),
        parse_mode='HTML'
    )


@router.message(Command("show_result"))
async def show_result_handler(message: types.Message, session: AsyncSession):
    flag = await check_admin_user(session, message.from_user.id)
    if not flag:
        await message.answer(
            'У вас нет админ прав!',
            parse_mode='HTML'
        )
        return

    today = datetime.datetime.now() + datetime.timedelta(days=1)
    today = today.strftime('%d.%m.%Y')
    events = await select_events_by_date(session, today)
    s = make_result_distrib(events)

    await message.answer(
        s,
        parse_mode='HTML',
        reply_markup=get_admin_distrb_result()
    )


@router.message(Command("send_link"))
async def send_link_handler(message: types.Message):
    months = get_month_full(config.directory_id)
    month_number_really = datetime.datetime.now().strftime('%m')
    builder = InlineKeyboardBuilder()

    for month in months['files']:
        month_number = int(month['name'].split('.')[0])
        if int(month_number_really) > month_number:
            continue
        builder.row(types.InlineKeyboardButton(
            text=month['name'], url="https://docs.google.com/spreadsheets/d/" + month['id'])
        )
    await message.answer(
        'Выберите месяц',
        reply_markup=builder.as_markup(),
    )
