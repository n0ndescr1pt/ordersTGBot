import asyncio

from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher

from data.config import TOKEN
from handlers.admin_handlers.add_rder_handlers import register_add_order_admin_handlers
from handlers.admin_handlers.edit_galery_handlers import register_edit_galery_admin_handlers
from handlers.admin_handlers.main_admin_handlers import register_main_admin_handlers
from handlers.admin_handlers.settings_handlers import register_settings_admin_handlers
from handlers.admin_handlers.upload_stat_handlers import register_upload_stat_admin_handlers
from handlers.user_handlers.about_us_handlers import register_aboutUs_user_handlers
from handlers.user_handlers.bonus_prog_handlers import register_bonus_user_handlers
from handlers.user_handlers.galery_handlers import register_galery_user_handlers
from handlers.user_handlers.main_handlers import register_main_user_handlers
from handlers.user_handlers.services_handlers import register_services_user_handlers
from utils.commands import set_commands

#сделать в кнопке баланс

async def register_handler(dp: Dispatcher):
    register_main_user_handlers(dp)
    register_bonus_user_handlers(dp)
    register_galery_user_handlers(dp)
    register_services_user_handlers(dp)
    register_aboutUs_user_handlers(dp)

    register_main_admin_handlers(dp)
    register_settings_admin_handlers(dp)
    register_edit_galery_admin_handlers(dp)
    register_upload_stat_admin_handlers(dp)
    register_add_order_admin_handlers(dp)


async def start_bot(bot: Bot):
    await set_commands(bot) #устанвливаем команды

async def main():

    token = TOKEN
    bot = Bot(token,parse_mode=ParseMode.HTML)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    await register_handler(dp)

    dp.startup.register(start_bot) #регистрируем команды

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
    print(__name__)