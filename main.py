import asyncio
import logging
import os
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command

# Import your handlers and states
from bot.handlers.start_handler import start_handler
from bot.handlers.department_handler import department_handler
from bot.handlers.semester_handler import semester_handler
from bot.handlers.subject_handler import subject_handler
from bot.handlers.material_handler import material_handler
from bot.states.user_states import UserState

load_dotenv()

# REPLACES LoggingMiddleware: Use standard python logging
logging.basicConfig(level=logging.INFO)

async def main():
    TOKEN = os.getenv("BOT_TOKEN", "8750084358")
    
    bot = Bot(token=TOKEN)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    # Register handlers using the 3.x way
    dp.message.register(start_handler, Command("start"))
    dp.message.register(department_handler, UserState.waiting_for_department)
    dp.message.register(semester_handler, UserState.waiting_for_semester)
    dp.message.register(subject_handler, UserState.waiting_for_subject)
    dp.message.register(material_handler, UserState.waiting_for_material_type)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot stopped")
