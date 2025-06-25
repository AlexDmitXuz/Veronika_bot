from aiogram.fsm.state import State, StatesGroup

# Состояния для редактирования сессии
class EditSession(StatesGroup):
    waiting_for_session_id = State()       # Ожидание ID сессии
    waiting_for_field = State()            # Ожидание выбора поля для редактирования
    waiting_for_new_value = State()        # Ожидание нового значения

# Состояние для рассылки
class BroadcastStates(StatesGroup):
    waiting_for_broadcast_text = State()   # Ожидание текста для рассылки
