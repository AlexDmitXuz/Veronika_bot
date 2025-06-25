from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def type_shoot_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура выбора типа фотосессии"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='💍 Свадебная', callback_data='wedding')],
        [InlineKeyboardButton(text='👨‍👩‍👧‍👦 Семейная', callback_data='family')],
        [InlineKeyboardButton(text='❤️ Love-story', callback_data='love_story')],
        [InlineKeyboardButton(text='📸 Индивидуальная', callback_data='individual')],
        [InlineKeyboardButton(text='🏠 Главное меню', callback_data='main_menu')]
    ])
    return keyboard

def confirm_booking() -> InlineKeyboardMarkup:
    """Клавиатура подтверждения или отмены бронирования"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='✅ Подтверждаю', callback_data='confirm_booking')],
        [InlineKeyboardButton(text='❌ Отмена', callback_data='cancel_booking')]
    ])

    return keyboard
