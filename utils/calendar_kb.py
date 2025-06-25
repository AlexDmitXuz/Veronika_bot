from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime
import calendar

def get_calendar(year: int = None, month: int = None) -> InlineKeyboardMarkup:
    """
    Создает инлайн-клавиатуру с календарем на указанный месяц и год.
    Если год и месяц не указаны, берется текущая дата.
    """
    if year is None or month is None:
        today = datetime.today()
        year = today.year
        month = today.month

    ru_month = {
        'January': 'Январь', 'February': 'Февраль', 'March': 'Март',
        'April': 'Апрель', 'May': 'Май', 'June': 'Июнь',
        'July': 'Июль', 'August': 'Август', 'September': 'Сентябрь',
        'October': 'Октябрь', 'November': 'Ноябрь', 'December': 'Декабрь'
    }
    month_name = datetime(year, month, 1).strftime('%B')

    buttons: list[list[InlineKeyboardButton]] = []

    # Заголовок с месяцем и годом
    buttons.append([
        InlineKeyboardButton(text=f"{ru_month[month_name]} {year}", callback_data="ignore")
    ])

    # Дни недели
    days = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']
    buttons.append([InlineKeyboardButton(text=day, callback_data="ignore") for day in days])

    # Месячный календарь (списки недель)
    month_calendar = calendar.monthcalendar(year, month)
    for week in month_calendar:
        row = []
        for day in week:
            if day == 0:
                row.append(InlineKeyboardButton(text=" ", callback_data="ignore"))
            else:
                callback_data = f"{year:04d}-{month:02d}-{day:02d}"
                row.append(InlineKeyboardButton(text=str(day), callback_data=callback_data))
        buttons.append(row)

    # Кнопки навигации (пред. и след. месяц, отмена)
    nav_buttons = [
        InlineKeyboardButton(text="«", callback_data=f"prev:{year}:{month}"),
        InlineKeyboardButton(text="Отмена", callback_data="cancel_booking"),
        InlineKeyboardButton(text="»", callback_data=f"next:{year}:{month}")
    ]
    buttons.append(nav_buttons)

    return InlineKeyboardMarkup(inline_keyboard=buttons)
