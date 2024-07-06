from aiogram import types, F, Router
from  keyboards.for_admin import get_admin_kb,get_admin_insert_kb,get_admin_distrb
from db import data
from keyboards.for_admin import  ChooseUser,DeleteUser,ChooseData
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
import datetime
from factory import get_event_by_name
router = Router()



@router.callback_query(F.data == "Админ-панель")
async def send_admin_requests(callback: types.CallbackQuery):
    await callback.message.answer(
        "Выберите действие",
        reply_markup=get_admin_kb()
    )
    await callback.answer()




@router.callback_query(F.data == "Показать всех работников")
async def send_admin_requests(callback: types.CallbackQuery):
     res =  data.select_all_players()
     s= ''
     for item in res:
         s = s + item[0] + ' | ' +  item[1] + '\n'
     await callback.message.answer(s)





@router.callback_query(F.data == "Добавить работника")
async def choose_id_ext(callback: types.CallbackQuery,state: FSMContext):
    await callback.message.answer(
        text="Введите TelegramID пользователя: ",
    )
    await state.set_state(ChooseUser.choosing_id_ext)




@router.callback_query(F.data == "Рассылка")
async def choose_id_ext(callback: types.CallbackQuery):
    await callback.message.answer(
        "Выберите дату рассылки",
        reply_markup=get_admin_distrb()
    )
    await callback.answer()


@router.callback_query(F.data == "Сегодня")
async def choose_id_ext(callback: types.CallbackQuery):
    today = datetime.datetime.now().strftime('%d.%m.%Y')
    print(today)
    print(get_event_by_name(today))
    await callback.answer()


@router.callback_query(F.data == "Завтра")
async def choose_id_ext(callback: types.CallbackQuery):
    today = datetime.datetime.now() + datetime.timedelta(days=1)
    today = today.strftime('%d.%m.%Y')
    print(today)
    print(get_event_by_name(today))
    await callback.answer()

@router.callback_query(F.data == "Выбрать дату")
async def choose_id_ext(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(
        "Введите дату в формате: День.Месяц.Год",
    )
    await state.set_state(ChooseData.date)



@router.message(ChooseData.date)
async def food_id_ext(message: Message, state: FSMContext):
    await state.update_data(date=message.text)
    date = await state.get_data()

    print(get_event_by_name(date['date']))



@router.message(DeleteUser.choosing_id_ext)
async def food_id_ext(message: Message, state: FSMContext):
    await state.update_data(choosing_id_ext=message.text)

    user_data = await state.get_data()

    await state.update_data(choosing_id_ext=message.text)
    await message.answer(
        text=f"Подтвердите выбранную информацию  ID: {user_data['choosing_id_ext']}",
        reply_markup=get_admin_insert_kb()
    )















@router.message(ChooseUser.choosing_id_ext)
async def food_id_ext(message: Message, state: FSMContext):
    await state.update_data(choosing_id_ext=message.text)
    await message.answer(
        text="Спасибо. Теперь, пожалуйста, выберите имя пользователя: ",
    )
    await state.set_state(ChooseUser.choosing_name)

@router.message(ChooseUser.choosing_name)
async def food_id_ext(message: Message, state: FSMContext):
    await state.update_data(choosing_name=message.text)

    user_data = await state.get_data()
    print(user_data)
    await message.answer(
        text=f"Подтвердите выбранную информацию  ID: {user_data['choosing_id_ext']} NAME: {user_data['choosing_name']}",
        reply_markup=get_admin_insert_kb()
    )

@router.callback_query(F.data == "Подтвердить")
async def choose_id_ext(callback: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    try:
        data.insert_player(user_data['choosing_id_ext'],user_data['choosing_name'])
        await state.clear()
        await callback.message.answer(
            text="Вставка произошла успешно",
        )
    except:
        data.delete_player(user_data['choosing_id_ext'])
        await state.clear()
        await callback.message.answer(
            text="Удаление произошло успешно",
        )



@router.callback_query(F.data == "Заполнить заново")
async def choose_id_ext(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()

    await callback.message.answer(
        "Выберите действие",
        reply_markup=get_admin_kb()
    )
    await callback.answer()

@router.callback_query(F.data == "Удалить работника")
async def choose_id_ext(callback: types.CallbackQuery,state: FSMContext):
    await callback.message.answer(
        text="Введите TelegramID пользователя: ",
    )
    await state.set_state(DeleteUser.choosing_id_ext)


@router.message(DeleteUser.choosing_id_ext)
async def food_id_ext(message: Message, state: FSMContext):
    await state.update_data(choosing_id_ext=message.text)

    user_data = await state.get_data()

    await state.update_data(choosing_id_ext=message.text)
    await message.answer(
        text=f"Подтвердите выбранную информацию  ID: {user_data['choosing_id_ext']}",
        reply_markup=get_admin_insert_kb()
    )
