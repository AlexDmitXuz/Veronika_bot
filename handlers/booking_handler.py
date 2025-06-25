from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from datetime import datetime

from config import load_config
from fsm.fsm_booking import Booking
from keyboards.booking_keyboard import *
from keyboards.main_menu_keyboard import main_menu_keyboard
from utils.calendar_kb import get_calendar
from utils.time_kb import time_booking
from database.db import add_photo_session

config = load_config()
photographer_id = config.admin_id

router = Router()

@router.callback_query(F.data=='booking')
async def booking_handler(callback:CallbackQuery, state: FSMContext):
    await callback.message.edit_text('Выбери тип съемки:', reply_markup=type_shoot_keyboard())
    await callback.answer()
    await state.set_state(Booking.type_shoot)

@router.callback_query(Booking.type_shoot)
async def booking_handler_type(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    admin_id = config.admin_id
    if callback.data == 'main_menu':
        await state.clear()
        await callback.message.edit_text("Бронирование отменено ❌", reply_markup=main_menu_keyboard(user_id=user_id, admin_id=admin_id))
        await callback.answer()
        await state.clear()
        await callback.answer()
        return
    await state.update_data(type_shoot=callback.data)
    await state.set_state(Booking.date)  # Сначала установить состояние
    await callback.message.edit_text("Выберите дату фотосессии", reply_markup=get_calendar())
    await callback.answer()

@router.callback_query(Booking.date)
async def booking_handler_date(callback: CallbackQuery, state: FSMContext):
    data = callback.data

    # Проверка формата YYYY-MM-DD
    try:
        selected_date = datetime.strptime(data, "%Y-%m-%d").date()
        today = datetime.today().date()

        if selected_date < today:
            await callback.answer("Нельзя выбрать прошедшую дату ❌", show_alert=True)
            return

        await state.update_data(date=selected_date)
        await callback.message.edit_text("Выберите время фотосессии", reply_markup=time_booking())
        await callback.answer()
        await state.set_state(Booking.time)
        return  # Выход после успешного выбора даты

    except ValueError:
        pass  # если это не дата — продолжаем проверку на next/prev/cancel

    if data.startswith("prev:") or data.startswith("next:"):
        parts = data.split(":")
        if len(parts) != 3:
            await callback.answer("Неверный формат данных")
            return

        _, year_str, month_str = parts
        year, month = int(year_str), int(month_str)
        if data.startswith("prev:"):
            if month == 1:
                year -= 1
                month = 12
            else:
                month -= 1
        else:  # next
            if month == 12:
                year += 1
                month = 1
            else:
                month += 1

        await callback.message.edit_reply_markup(reply_markup=get_calendar(year, month))
        await callback.answer()

    elif data == "cancel_booking":
        user_id = callback.from_user.id
        admin_id = config.admin_id
        await callback.message.edit_text("Бронирование отменено ❌", reply_markup=main_menu_keyboard(user_id=user_id, admin_id=admin_id))
        await callback.answer()
        await state.clear()

    else:
        await callback.answer()


@router.callback_query(Booking.time)
async def booking_handler_time(callback: CallbackQuery, state: FSMContext):
    if callback.data.startswith("time:"):
        time_selected = callback.data.split("time:")[1]
        await state.update_data(time=time_selected)
        data = await state.get_data()
        await callback.message.edit_text(
            f"<b>Подтвердите бронь</b>:\n\n"
            f"📸 Тип съёмки: <b>{data['type_shoot']}</b>\n"
            f"📅 Дата: <b>{data['date']}</b>\n"
            f"🕒 Время: <b>{data['time']}</b>",
            reply_markup=confirm_booking(),
            parse_mode="HTML"
        )
        await state.set_state(Booking.confirm)
    await callback.answer()


@router.callback_query(Booking.confirm)
async def booking_handler_confirm(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if data == "cancel_booking":
        user_id = callback.from_user.id
        admin_id = config.admin_id
        await callback.message.edit_text("Бронирование отменено ❌", reply_markup=main_menu_keyboard(user_id=user_id, admin_id=admin_id))
        await callback.answer()
        await state.clear()
    else:
        user_id = callback.from_user.id
        admin_id = config.admin_id
        await callback.message.edit_text('Запись подтверждена ✅', reply_markup=main_menu_keyboard(user_id=user_id, admin_id=admin_id))

        text = (
            f"📸 Новая заявка!\n\n"
            f"👤 Клиент: @{callback.from_user.username or 'Без username'}\n"
            f"🆔 ID: {callback.from_user.id}\n"
            f"Тип: {data['type_shoot']}\n"
            f"Дата: {data['date']}\n"
            f"Время: {data['time']}"
        )
        await callback.bot.send_message(chat_id=photographer_id, text=text)

        await add_photo_session(
            user_id=callback.from_user.id,
            username=callback.from_user.username,
            session_type=data['type_shoot'],
            session_date=data['date'],  # формат ГГГГ-ММ-ДД
            session_time=data['time'],  # формат ЧЧ:ММ
            )

        await state.clear()
        await callback.answer()







