import asyncio
import logging
from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from handlers import admin, start
from config import bot
from middlewares import DataBaseSession
from db.engine import session_maker


async def main():
    #  await create_db()
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_routers(start.router, admin.router)
    dp.update.middleware(DataBaseSession(session_pool=session_maker))
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
