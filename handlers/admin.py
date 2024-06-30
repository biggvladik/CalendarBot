from aiogram import types, F, Router
from  keyboards.for_admin import get_admin_kb
router = Router()



@router.callback_query(F.data == "Админ-панель")
async def send_admin_requests(callback: types.CallbackQuery):
    await callback.message.answer(
        "Выберите действие",
        reply_markup=get_admin_kb()
    )
    await callback.answer()