import asyncio

from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher

from data.config import TOKEN
from handlers.user_handlers.about_us_handlers import register_aboutUs_user_handlers
from handlers.user_handlers.bonus_prog_handlers import register_bonus_user_handlers
from handlers.user_handlers.galery_handlers import register_galery_user_handlers
from handlers.user_handlers.main_handlers import register_main_user_handlers
from handlers.user_handlers.services_handlers import register_services_user_handlers


def register_handler(dp: Dispatcher) -> None:
    register_main_user_handlers(dp)
    register_bonus_user_handlers(dp)
    register_galery_user_handlers(dp)
    register_services_user_handlers(dp)
    register_aboutUs_user_handlers(dp)
    #register_payment_handlers(dp)
    #register_admin_handlers(dp)
    pass

async def main():

    token = TOKEN
    bot = Bot(token,parse_mode=ParseMode.MARKDOWN_V2)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    register_handler(dp)

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
    print(__name__)