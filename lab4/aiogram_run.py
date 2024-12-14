import asyncio
import logging
import os
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
from bot_handlers.bot_handlers import router


# Подгрузка .env
load_dotenv()


# Инициализация логгирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


# Инициализация бота
bot = Bot(token=os.getenv('BOT_TOKEN'))
dp = Dispatcher(storage=MemoryStorage())


# Функция, подключающая имеющиеся хендлеры и начинающая поллинг
async def main():
    dp.include_router(router)
    await dp.start_polling(bot) 


# Запуск бота
if __name__ == "__main__":
    asyncio.run(main())