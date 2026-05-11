import asyncio
import logging
import os
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
# In aiogram 3.x, filters are more explicit
from aiogram.filters import Command

# Import your handlers and states
from bot.handlers.start_handler import start_handler
from bot.handlers.department_handler import department_handler
from bot.handlers.semester_handler import semester_handler
from bot.handlers.subject_handler import subject_handler
# Fixed a typo from your original code (Userstate -> UserState)
from bot.handlers.material_handler import material_handler
from bot.states.user_states import UserState

load_dotenv()

# Setup logging (replaces LoggingMiddleware which was removed in 3.x)
logging.basicConfig(level=logging.INFO)

async def main():
    TOKEN = os.getenv("BOT_TOKEN", "8750084358")
    
    # Initialize Bot and Dispatcher
    bot = Bot(token=TOKEN)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    # Register handlers
    # Use .register() or decorators. Note: 'commands' is now the Command filter
    dp.message.register(start_handler, Command("start"))
    
    # In 3.x, the state filter is mandatory if you want to filter by state
    dp.message.register(department_handler, UserState.waiting_for_department)
    dp.message.register(semester_handler, UserState.waiting_for_semester)
    dp.message.register(subject_handler, UserState.waiting_for_subject)
    
    # Note: Ensure unit_handler is imported in your real project
    # dp.message.register(unit_handler, UserState.waiting_for_unit) 
    
    dp.message.register(material_handler, UserState.waiting_for_material_type)

    # Start polling
    # skip_updates is handled by deleting webhook before polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot stopped")
