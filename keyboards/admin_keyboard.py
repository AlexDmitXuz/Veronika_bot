from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def admin_menu_keyboard() -> InlineKeyboardMarkup:
    """Главное меню админа"""
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📋 Просмотреть заявки", callback_data="admin_view_requests")],
        [InlineKeyboardButton(text="✏️ Редактировать заявки", callback_data="admin_edit_requests")],
        [InlineKeyboardButton(text="📣 Рассылка акций", callback_data="admin_send_promos")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="admin_back")]
    ])

    return kb

def admin_menu_edit_value() -> InlineKeyboardMarkup:
    """Выбор поля для редактирования заявки"""
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='📅 Дата', callback_data='admin_edit_date')],
        [InlineKeyboardButton(text='⏰ Время', callback_data='admin_edit_time')],
        [InlineKeyboardButton(text='🎞️ Тип фотосессии', callback_data='admin_edit_type_session')],
        [InlineKeyboardButton(text='📌 Статус заявки', callback_data='admin_edit_status')],
        [InlineKeyboardButton(text='🏠 Главное меню', callback_data='admin_menu_back')]
    ])

    return kb

def admin_status() -> InlineKeyboardMarkup:
    """Выбор статуса заявки"""
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='🆕 новая', callback_data='status_new')],
        [InlineKeyboardButton(text='✅ подтвержденная', callback_data='status_confirmed')],
        [InlineKeyboardButton(text='✔️ выполненная', callback_data='status_completed')],
        [InlineKeyboardButton(text='❌ отмененная', callback_data='status_cancelled')],
        [InlineKeyboardButton(text='🏠 Главное меню', callback_data='admin_menu_back')]
    ])

    return kb

def admin_promo_type() -> InlineKeyboardMarkup:
    """Выбор группы клиентов для рассылки"""
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📬 Все клиенты", callback_data="promo_all_clients")],
        [InlineKeyboardButton(text="🆕 Новые заявки", callback_data="promo_new")],
        [InlineKeyboardButton(text="✅ Подтверждённые", callback_data="promo_confirmed")],
        [InlineKeyboardButton(text="📁 Выполненные", callback_data="promo_done")],
        [InlineKeyboardButton(text="❌ Отменённые", callback_data="promo_canceled")],
        [InlineKeyboardButton(text='Главное меню', callback_data='admin_menu_back')]
    ])
    return kb

def admin_menu_back() -> InlineKeyboardMarkup:
    """Кнопка назад к админ-меню"""
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Назад", callback_data="admin")]
    ])

    return kb
