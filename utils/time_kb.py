from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def time_booking() -> InlineKeyboardMarkup:
    times = [f"{hour:02d}:00" for hour in range(10, 21)]  # с 10:00 до 20:00
    keyboard = []

    row = []
    for i, time in enumerate(times, 1):
        row.append(InlineKeyboardButton(text=time, callback_data=f"time:{time}"))
        if i % 4 == 0:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)

    # Кнопка "Другое время"
    keyboard.append([
        InlineKeyboardButton(text="🕒 Другое время", callback_data="time:other")
    ])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)
