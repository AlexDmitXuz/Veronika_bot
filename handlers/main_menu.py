from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from keyboards.main_menu_keyboard import main_menu_keyboard
from database.db import register_client
from config import load_config

router = Router()

config = load_config()
admin_id = config.admin_id

# Обработка команды /start
@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    await register_client(message.from_user)
    user_id = message.from_user.id
    admin_id = config.admin_id
    kb = main_menu_keyboard(user_id=user_id, admin_id=admin_id)


    await message.answer(
    "Привет! 👋 Я — Вероника, твой фотограф с опытом и профессиональной техникой 📸\n"
    "Сохраняю важные моменты для молодожёнов, семей, будущих мам и индивидуальных клиентов.\n"
    "Качество, скорость и индивидуальный подход — чтобы твои воспоминания были живыми и яркими.\n\n"
    "Выбери, какая фотосессия тебе интересна, и давай создадим что-то особенное вместе!", reply_markup=kb)

# Обработка возврата в главное меню по инлайн-кнопке
@router.callback_query(F.data == "main_menu")
async def main_menu(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await register_client(callback.from_user)
    user_id = callback.from_user.id
    admin_id = config.admin_id
    kb = main_menu_keyboard(user_id=user_id, admin_id=admin_id)

    await callback.message.edit_text("Привет! Я бот-фотограф 📸", reply_markup=kb)
    await callback.answer()
