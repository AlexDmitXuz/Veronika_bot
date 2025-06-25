from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def contacts_kb() -> InlineKeyboardMarkup:
    """Клавиатура с контактными ссылками"""
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='📸 Instagram', url='https://www.instagram.com/abdulmanova.veronica')],
        [InlineKeyboardButton(text='👥 ВКонтакте', url='https://vk.com/cutietwig')],
        [InlineKeyboardButton(text='✉️ Telegram', url='https://t.me/cutietwig')],
        [InlineKeyboardButton(text='🏠 Главное меню', callback_data='main_menu')]
    ])

    return kb
