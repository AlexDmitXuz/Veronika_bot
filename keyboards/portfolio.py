from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def portfolio_kb() -> InlineKeyboardMarkup:
    """Выбор типа фотосессии в портфолио"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='💍 Свадебная', callback_data='portfolio_wedding')],
        [InlineKeyboardButton(text='❤️ Love-story', callback_data='portfolio_lovestory')],
        [InlineKeyboardButton(text='👤 Индивидуальная', callback_data='portfolio_individual')],
        [InlineKeyboardButton(text='👨‍👩‍👧‍👦 Семейная', callback_data='portfolio_family')],
        [InlineKeyboardButton(text='🏠 Главное меню', callback_data='main_menu')]
    ])

    return keyboard

def photos_more_kb(url: str = 'https://www.instagram.com/abdulmanova.veronica') -> InlineKeyboardMarkup:
    """Клавиатура с кнопками 'Еще фотографии' и 'Главное меню'"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='📷 Еще фотографии', url=url)],
        [InlineKeyboardButton(text='🏠 Главное меню', callback_data='main_menu')]
    ])

    return keyboard

# Для удобства, если нужны отдельные функции:

def wedding_kb() -> InlineKeyboardMarkup:
    return photos_more_kb()

def family_kb() -> InlineKeyboardMarkup:
    return photos_more_kb()

def lovestory_kb() -> InlineKeyboardMarkup:
    return photos_more_kb()

def individual_kb() -> InlineKeyboardMarkup:
    return photos_more_kb()
