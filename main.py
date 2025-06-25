from middlewares.db_pool import DbPoolMiddleware
import asyncio
from aiogram import Bot, Dispatcher, types, Router
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from config import load_config
from aiogram.client.default import DefaultBotProperties
from handlers import booking_handler, contacts, main_menu, portfolio, admin_handler, calendar_handler
from database.db import create_pool

config = load_config()
router=Router()
bot = Bot(
    token=config.bot_token,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher(storage=MemoryStorage())

async def main():
    pool=await create_pool()
    dp.message.middleware(DbPoolMiddleware(pool))
    dp.callback_query.middleware(DbPoolMiddleware(pool))
    dp.include_router(booking_handler.router)
    dp.include_router(calendar_handler.router)
    dp.include_router(admin_handler.router)
    dp.include_router(contacts.router)
    dp.include_router(main_menu.router)
    dp.include_router(portfolio.router)
  # это важно!

    await dp.start_polling(bot, dp_pool=pool)

if __name__ == "__main__":
    asyncio.run(main())
