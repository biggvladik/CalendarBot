import traceback

from aiogram import types, F, Router
from keyboards.for_admin import get_admin_kb, get_admin_insert_kb, get_admin_distrb, get_admin_reply, \
    get_admin_distrb_result
from db import data
from keyboards.for_admin import ChooseUser, DeleteUser, ChooseData, ChooseDataResult
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
import datetime
from factory import get_event_by_name, make_str, make_distrib, make_result_distrib, make_full_str
from config import bot

router = Router()


@router.callback_query(F.data == "Админ-панель")
async def send_admin_requests(callback: types.CallbackQuery):
    # Авторизация
    flag = data.check_admin_user(callback.from_user.id)
    if not flag:
        await callback.message.answer(
            "У вас нет админ прав | Вы не авторизованы",
        )
    else:
        await callback.message.answer(
            "Выберите действие",
            reply_markup=get_admin_kb()
        )
    await callback.answer()


@router.callback_query(F.data == "cancel_result")
async def send_cancel_admin_distrib(callback: types.CallbackQuery):
    await callback.message.answer(
        text='Выберите действие',
        reply_markup=get_admin_distrb()
    )
    await callback.answer()


@router.callback_query(F.data == "cancel_distrib")
async def send_cancel_admin_distrib(callback: types.CallbackQuery):
    await callback.message.answer(
        text='Выберите действие',
        reply_markup=get_admin_kb()
    )
    await callback.answer()


@router.callback_query(F.data == "Показать всех работников")
async def send_admin_requests(callback: types.CallbackQuery):
    res = data.select_all_players()
    s = ''
    for item in res:
        s = s + item[0] + ' | ' + item[1] + '\n'
    await callback.message.answer(s)


@router.callback_query(F.data == "Добавить работника")
async def add_worker(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(
        text="Введите TelegramID пользователя: ",
    )
    await state.set_state(ChooseUser.choosing_id_ext)


@router.callback_query(F.data == "Рассылка")
async def pick_distrib(callback: types.CallbackQuery):
    await callback.message.answer(
        "Выберите дату рассылки",
        reply_markup=get_admin_distrb()
    )
    await callback.answer()


@router.callback_query(F.data == "Сегодня")
async def pick_distrib_today(callback: types.CallbackQuery):
    today = datetime.datetime.now().strftime('%d.%m.%Y')
    all_players = data.select_all_players_new()
    events = get_event_by_name(today)
    res = make_distrib(all_players, events)
    res_s = ''
    res_false = ''
    send_events = []
    for event in res:
        print(event['event'])
        try:
            if not event['event']:
                continue
            await bot.send_message(int(event['id']), make_full_str(make_str(event['event'])), parse_mode='HTML',
                                   reply_markup=get_admin_reply())
            data.insert_message_logs(today, event)
            res_s += make_str(event['event'])
            send_events.append(event['event'])

        except Exception:
            res_false += make_str(event['event'])
            print(traceback.format_exc(), event)

    await callback.message.answer(
        make_full_str('Отправленные события:\n' + res_s),
        parse_mode='HTML'
    )
    for event in events:
        if not event in send_events:
            print(event)
            res_false += make_str([event])

    await callback.message.answer(
        make_full_str('Неотправленные события:\n' + res_false),
        parse_mode='HTML'
    )

    await callback.answer()


@router.callback_query(F.data == "Завтра")
async def pick_distrib_tommorow(callback: types.CallbackQuery):
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
            await bot.send_message(int(event['id']), make_full_str(make_str(event['event'])), parse_mode='HTML',
                                   reply_markup=get_admin_reply())
            data.insert_message_logs(today, event)
            res_s += make_str(event['event'])
        except Exception:
            pass
    if res_s:
        await callback.message.answer(
            make_full_str(res_s),
            parse_mode='HTML'
        )
    else:
        await callback.message.answer(
            'Ничего отправлено не было!',
            parse_mode='HTML'
        )
    await callback.answer()


@router.callback_query(F.data == "Выбрать дату")
async def pick_distrib_date(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(
        "Введите дату в формате: День.Месяц.Год",
    )
    await state.set_state(ChooseData.date)


@router.message(ChooseData.date)
async def pick_distrib_date_requests(message: Message, state: FSMContext):
    await state.update_data(date=message.text)
    date = await state.get_data()

    all_players = data.select_all_players_new()
    events = get_event_by_name(date['date'])
    res = make_distrib(all_players, events)
    res_s = ''

    for event in res:
        if not event['event']:
            continue
        try:
            if make_str(event['event']) == 'Расписание не найдено!':
                continue
            await bot.send_message(int(event['id']), make_full_str(make_str(event['event'])), parse_mode='HTML',
                                   reply_markup=get_admin_reply())
            data.insert_message_logs(date['date'], event)
            res_s += make_str(event['event'])

        except Exception:
            pass
    if res_s:
        await message.answer(
            make_full_str(res_s),
            parse_mode='HTML'
        )
    else:
        await message.answer(
            'Ничего отправлено не было!',
            parse_mode='HTML'
        )


@router.callback_query(F.data == "reply_user")
async def reply_user_request(callback: types.CallbackQuery):
    date = callback.message.text.split('\n')[0].split()[1].strip()
    print(date, callback.from_user.id)
    data.change_status_message(date, callback.from_user.id)
    await bot.send_message(callback.from_user.id, 'Подтверждение произошло успешно!')


@router.callback_query(F.data == "result distrib")
async def get_result_distrib(callback: types.CallbackQuery):
    await callback.message.answer(
        "Выберите дату событий",
        reply_markup=get_admin_distrb_result()
    )
    await callback.answer()


@router.callback_query(F.data == "today_result")
async def get_result_distrib_today(callback: types.CallbackQuery):
    today = datetime.datetime.now().strftime('%d.%m.%Y')
    events = data.select_events_by_date(today)
    s = make_result_distrib(events)

    await callback.message.answer(
        s,
        parse_mode='HTML',
        reply_markup=get_admin_distrb_result()
    )
    await callback.answer()


@router.callback_query(F.data == "tommorow_result")
async def get_result_distrib_tommorow(callback: types.CallbackQuery):
    today = datetime.datetime.now() + datetime.timedelta(days=1)
    today = today.strftime('%d.%m.%Y')
    events = data.select_events_by_date(today)
    s = make_result_distrib(events)

    if s.strip() == '':
        s = 'События не найдены!'
    await callback.message.answer(
        s,
        parse_mode='HTML',
        reply_markup=get_admin_distrb_result()
    )
    await callback.answer()


@router.callback_query(F.data == "choose_date_result")
async def get_result_distrib_date(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(
        "Введите дату в формате: День.Месяц.Год",
    )
    await state.set_state(ChooseDataResult.date)


@router.message(ChooseDataResult.date)
async def get_result_distrib_date_request(message: Message, state: FSMContext):
    await state.update_data(date=message.text)
    date = await state.get_data()

    events = data.select_events_by_date(date['date'])
    s = make_result_distrib(events)
    if s.strip() == '':
        s = 'События не найдены!'
    await message.answer(
        s,
        parse_mode='HTML',
        reply_markup=get_admin_distrb_result()
    )


@router.message(DeleteUser.choosing_id_ext)
async def delete_user_request_id(message: Message, state: FSMContext):
    await state.update_data(choosing_id_ext=message.text)

    user_data = await state.get_data()

    await state.update_data(choosing_id_ext=message.text)
    await message.answer(
        text=f"Подтвердите выбранную информацию  ID: {user_data['choosing_id_ext']}",
        reply_markup=get_admin_insert_kb()
    )


@router.message(ChooseUser.choosing_id_ext)
async def delete_user_request_name(message: Message, state: FSMContext):
    await state.update_data(choosing_id_ext=message.text)
    await message.answer(
        text="Спасибо. Теперь, пожалуйста, выберите имя пользователя: ",
    )
    await state.set_state(ChooseUser.choosing_name)


@router.message(ChooseUser.choosing_name)
async def delete_user_request_reply(message: Message, state: FSMContext):
    await state.update_data(choosing_name=message.text)

    user_data = await state.get_data()
    await message.answer(
        text=f"Подтвердите выбранную информацию  ID: {user_data['choosing_id_ext']} NAME: {user_data['choosing_name']}",
        reply_markup=get_admin_insert_kb()
    )


@router.callback_query(F.data == "Подтвердить")
async def delete_user_request_finish(callback: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    print(user_data)
    try:
        flag = data.insert_player(user_data['choosing_id_ext'], user_data['choosing_name'])
        await state.clear()
        if not flag:
            await callback.message.answer(
                text="Вставка произошла успешно",
                reply_markup=get_admin_kb()

            )
        else:
            await callback.message.answer(
                text=flag,
                reply_markup=get_admin_kb()
            )

    except Exception:
        print(traceback.format_exc())
        data.delete_player(user_data['choosing_id_ext'])
        await state.clear()
        await callback.message.answer(
            text="Удаление произошло успешно",
            reply_markup=get_admin_kb()
        )


@router.callback_query(F.data == "Заполнить заново")
async def pick_again(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()

    await callback.message.answer(
        "Выберите действие",
        reply_markup=get_admin_kb()
    )
    await callback.answer()


@router.callback_query(F.data == "Удалить работника")
async def delete_worker_id(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(
        text="Введите TelegramID пользователя: ",
    )
    await state.set_state(DeleteUser.choosing_id_ext)


@router.message(DeleteUser.choosing_id_ext)
async def delete_worker_reply(message: Message, state: FSMContext):
    await state.update_data(choosing_id_ext=message.text)

    user_data = await state.get_data()

    await state.update_data(choosing_id_ext=message.text)
    await message.answer(
        text=f"Подтвердите выбранную информацию  ID: {user_data['choosing_id_ext']}",
        reply_markup=get_admin_insert_kb()
    )
