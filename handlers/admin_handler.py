from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, InlineKeyboardButton

from keyboards.admin_keyboard import (
    admin_menu_keyboard, admin_menu_edit_value,
    admin_status, admin_promo_type, admin_menu_back
)
from keyboards.main_menu_keyboard import main_menu_keyboard
from keyboards.booking_keyboard import type_shoot_keyboard

from database.db import get_all_sessions, update_session_field, archive_old_sessions
from fsm.fsm_admin_esit_session import EditSession, BroadcastStates
from utils.calendar_kb import get_calendar
from utils.time_kb import time_booking
from config import load_config
from datetime import datetime

config = load_config()
admin = config.admin_id

router = Router()

@router.callback_query(lambda c: c.data == "admin")
async def admin_menu(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text("Меню фотографа:", reply_markup=admin_menu_keyboard())

@router.callback_query(lambda c: c.data == "admin_view_requests")
async def view_requests(callback: CallbackQuery):
    sessions = await get_all_sessions()
    if not sessions:
        await callback.message.edit_text("Заявок пока нет.", reply_markup=admin_menu_keyboard())
        return

    response = "📋 Список заявок:\n\n"
    for s in sessions:
        response += (
            f"ID: {s['id']}\n"
            f"Пользователь: @{s['username']} (ID: {s['user_id']})\n"
            f"Тип съемки: {s['session_type']}\n"
            f"Дата: {s['session_date']}\n"
            f"Время: {s['session_time']}\n"
            f"Статус: {s['status']}\n\n"
        )
    await callback.message.edit_text(response, reply_markup=admin_menu_keyboard())

@router.callback_query(lambda c: c.data == "admin_edit_requests")
async def edit_session_start(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Введите ID заявки для редактирования:", reply_markup=admin_menu_back())
    await state.set_state(EditSession.waiting_for_session_id)

@router.message(EditSession.waiting_for_session_id)
async def process_session_id(message: Message, state: FSMContext):
    session_id = message.text.strip()
    if not session_id.isdigit():
        await message.answer("ID должен быть числом. Попробуйте снова.", reply_markup=admin_menu_back())
        return
    await state.update_data(session_id=int(session_id))
    await message.answer("Что хотите изменить? (дата, время, тип, статус)", reply_markup=admin_menu_edit_value())
    await state.set_state(EditSession.waiting_for_field)

@router.callback_query(EditSession.waiting_for_field)
async def process_field_choice(callback: CallbackQuery, state: FSMContext):
    field_map = {
        "admin_edit_date": "дата",
        "admin_edit_time": "время",
        "admin_edit_type_session": "тип",
        "admin_edit_status": "статус"
    }

    if callback.data not in field_map:
        await callback.message.edit_text("Можно изменить только: дата, время, тип или статус. Попробуйте снова.")
        return

    field = field_map[callback.data]
    await state.update_data(field=field)

    if field == 'дата':
        await callback.message.edit_text('Выберите новую дату бронирования:', reply_markup=get_calendar())
    elif field == 'время':
        await callback.message.edit_text('Выберите новое время бронирования:', reply_markup=time_booking())
    elif field == 'тип':
        await callback.message.edit_text('Измените тип фотосессии:', reply_markup=type_shoot_keyboard())
    elif field == 'статус':
        await callback.message.edit_text('Измените статус заявки:', reply_markup=admin_status())

    await state.set_state(EditSession.waiting_for_new_value)

@router.callback_query(EditSession.waiting_for_new_value)
async def process_new_value(callback: CallbackQuery, state: FSMContext):
    if callback.data == 'admin_menu_back':
        await callback.message.edit_text('Меню фотографа:', reply_markup=admin_menu_keyboard())
        await state.clear()
        return

    data = await state.get_data()
    session_id = data["session_id"]
    field = data["field"]

    if callback.data.startswith("time:"):
        new_value = callback.data.split("time:")[1]
    else:
        new_value = callback.data

    field_map = {
        "дата": "session_date",
        "время": "session_time",
        "тип": "session_type",
        "статус": "status"
    }
    db_field = field_map[field]

    if db_field == "session_date":
        try:
            new_value = datetime.strptime(new_value, "%Y-%m-%d").date()
        except ValueError:
            await callback.message.edit_text("Неверный формат даты. Ожидается ГГГГ-ММ-ДД. Попробуйте снова.")
            return

    await update_session_field(session_id, db_field, new_value)
    await archive_old_sessions()
    await callback.message.edit_text(f"Заявка {session_id} обновлена: {field} -> {new_value}", reply_markup=admin_menu_keyboard())
    await state.clear()
    await callback.answer()

@router.callback_query(lambda c: c.data == "admin_send_promos")
async def send_promos(callback: CallbackQuery):
    await callback.message.edit_text("Выберите группу для рассылки:", reply_markup=admin_promo_type())

@router.callback_query(lambda c: c.data == "admin_back")
async def admin_back(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    user_id = callback.from_user.id
    admin_id = config.admin_id
    kb = main_menu_keyboard(user_id=user_id, admin_id=admin_id)
    await callback.message.edit_text("Привет! Я бот-фотограф 📸", reply_markup=kb)


@router.callback_query(F.data.startswith("promo_"))
async def choose_recipient_group(callback: CallbackQuery, state: FSMContext, dp_pool):
    target = callback.data.split("_")[1]

    query_map = {
        "all": "SELECT DISTINCT user_id FROM clients",
        "new": "SELECT DISTINCT user_id FROM photo_tg_bot WHERE status = 'новая'",
        "confirmed": "SELECT DISTINCT user_id FROM photo_tg_bot WHERE status = 'подтверждена'",
        "done": "SELECT DISTINCT user_id FROM archive_sessions WHERE status = 'выполнена'",
        "canceled": "SELECT DISTINCT user_id FROM archive_sessions WHERE status = 'отменена'",
    }

    query = query_map.get(target)
    if not query:
        await callback.message.edit_text("Ошибка выбора категории получателей.")
        return

    async with dp_pool.acquire() as conn:
        users = await conn.fetch(query)

    if not users:
        await callback.message.answer("В этой группе пока нет клиентов. Выберите другую группу.")
        await callback.message.edit_text("Выберите группу для рассылки:", reply_markup=admin_promo_type())
        return

    user_ids = [record["user_id"] for record in users]

    await state.update_data(recipients=user_ids)
    await callback.message.edit_text(f"Получателей: {len(user_ids)}. Введите текст рассылки:")
    await state.set_state(BroadcastStates.waiting_for_broadcast_text)

@router.message(BroadcastStates.waiting_for_broadcast_text)
async def broadcast_text_handler(message: Message, state: FSMContext, dp_pool):
    data = await state.get_data()
    recipients = data.get("recipients", [])
    text = message.text

    if not recipients:
        await message.answer("Список получателей пуст, рассылка отменена.")
        await state.clear()
        return

    success_count = 0
    failed_users = []

    async with dp_pool.acquire() as conn:
        for user_id in recipients:
            try:
                await message.bot.send_message(chat_id=user_id, text=text)
                success_count += 1
            except Exception:
                failed_users.append(user_id)

    await message.answer(f"Рассылка завершена.\nОтправлено: {success_count}\n"
                         f"Не доставлено: {len(failed_users)}", reply_markup=admin_menu_keyboard())
    await state.clear()
