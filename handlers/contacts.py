from aiogram import Router, F
from aiogram.types import CallbackQuery
from keyboards.contacts import contacts_kb

router = Router()

@router.callback_query(F.data == "contacts")
async def contact_callback(callback: CallbackQuery):
    """Обработка кнопки 'Контакты' — выводит инлайн-кнопки со ссылками"""
    await callback.message.edit_text(
        "📲 Выберите один из способов связи:",
        reply_markup=contacts_kb()
    )
    await callback.answer()
