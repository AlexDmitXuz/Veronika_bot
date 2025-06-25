from aiogram.fsm.state import State, StatesGroup

# Состояния для оформления заявки на фотосессию
class Booking(StatesGroup):
    type_shoot = State()   # Выбор типа съёмки
    date = State()         # Выбор даты
    time = State()         # Выбор времени
    confirm = State()      # Подтверждение заявки
