from typing import Optional
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder
from factory import get_month
import config
class MonthCallbackFactory(CallbackData, prefix="fabnum"):
    action: str
    value: Optional[str] = None


def get_keyboard_fab():
    builder = InlineKeyboardBuilder()
    button_text = get_month(config.directory_id)

    builder.button(
        text=button_text[0], callback_data=MonthCallbackFactory(action="pick_month", value=button_text[0])
    )
    builder.button(
        text=button_text[1], callback_data=MonthCallbackFactory(action="pick_month", value=button_text[1])
    )
    builder.adjust(2)
    return builder.as_markup()

