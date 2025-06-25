from aiogram import F, Router
from aiogram.types import CallbackQuery, FSInputFile
from keyboards.main_menu_keyboard import main_menu_keyboard
from keyboards.portfolio import *
from aiogram.utils.media_group import MediaGroupBuilder
from pathlib import Path
from config import load_config

config=load_config()
router = Router()

BASE_DIR = Path(__file__).parent.parent
PORTFOLIO_DIR = BASE_DIR / "portfolio"


async def send_portfolio(callback: CallbackQuery, folder: str, caption: str, keyboard):
    media = MediaGroupBuilder(caption=caption)
    folder_path = PORTFOLIO_DIR / folder

    for i in range(1, 7):
        file_path = folder_path / f"{i}.jpg"
        if file_path.exists():
            media.add_photo(FSInputFile(file_path))

    await callback.message.answer_media_group(media=media.build())
    await callback.message.answer("Выберите действие:", reply_markup=keyboard)


@router.callback_query(F.data == 'portfolio')
async def portfolio(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text('Выберите тип съемки:', reply_markup=portfolio_kb())


@router.callback_query(F.data == 'portfolio_wedding')
async def portfolio_wedding(callback: CallbackQuery):
    await callback.answer()
    await send_portfolio(callback, "wedding", "Свадебная фотосессия", wedding_kb())


@router.callback_query(F.data == 'portfolio_individual')
async def portfolio_individual(callback: CallbackQuery):
    await callback.answer()
    await send_portfolio(callback, "individual", "Индивидуальная фотосессия", individual_kb())


@router.callback_query(F.data == 'portfolio_lovestory')
async def portfolio_lovestory(callback: CallbackQuery):
    await callback.answer()
    await send_portfolio(callback, "love-story", "Love-story фотосессия", lovestory_kb())


@router.callback_query(F.data == 'portfolio_family')
async def portfolio_family(callback: CallbackQuery):
    await callback.answer()
    await send_portfolio(callback, "family", "Семейная фотосессия", family_kb())


@router.callback_query(F.data == 'portfolio_cancel')
async def portfolio_cancel(callback: CallbackQuery):
    await callback.answer()
    admin_id = config.admin_id
    user_id=callback.from_user.id
    await callback.message.edit_text('Главное меню:', reply_markup=main_menu_keyboard(user_id=user_id, admin_id=admin_id))
