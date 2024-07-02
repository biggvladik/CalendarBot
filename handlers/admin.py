from aiogram import types, F, Router
from  keyboards.for_admin import get_admin_kb
from db import data
from keyboards.for_admin import  ChooseUser
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
async def send_admin_requests(callback: types.CallbackQuery):
     res =  data.select_all_players()
     s= ''
     for item in res:
         s = s + item[0] + ' | ' +  item[1] + '\n'
     await callback.message.answer(s)