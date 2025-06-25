from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def main_menu_keyboard(user_id: int, admin_id: int) -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="📅 Запись", callback_data="booking")],
        [InlineKeyboardButton(text="🖼️ Портфолио", callback_data="portfolio")],
        [InlineKeyboardButton(text="📞 Контакты", callback_data="contacts")]
    ]

    if user_id == admin_id:
        buttons.append([InlineKeyboardButton(text="Админ", callback_data="admin")])

    return InlineKeyboardMarkup(inline_keyboard=buttons)
