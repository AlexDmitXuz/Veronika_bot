from aiogram import Router, F
from aiogram.types import CallbackQuery
from utils.calendar_kb import get_calendar

router = Router()

@router.callback_query(F.data.startswith("prev:") | F.data.startswith("next:"))
async def switch_month(callback: CallbackQuery):
    # Разбор данных: формат "prev:2025:6" или "next:2025:8"
    try:
        _, year_str, month_str = callback.data.split(":")
        year, month = int(year_str), int(month_str)
    except (ValueError, IndexError):
        await callback.answer("Ошибка данных календаря", show_alert=True)
        return

    # Изменение месяца
    if callback.data.startswith("prev:"):
        month -= 1
        if month < 1:
            month = 12
            year -= 1
    else:  # "next:"
        month += 1
        if month > 12:
            month = 1
            year += 1

    # Обновление клавиатуры
    await callback.message.edit_reply_markup(reply_markup=get_calendar(year, month))
    await callback.answer()
