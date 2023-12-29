import time

from aiogram import types, Dispatcher, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from data.config import password
from keyboards.admin_kb import main_admin_kb, cancel_kb, settings_kb
from keyboards.user_kb import main_kb
from states import CheckAdmin


async def setting(callback: types.CallbackQuery):
    await callback.message.edit_text(f"Настройки", reply_markup=settings_kb())









def register_settings_admin_handlers(dp: Dispatcher):
    dp.callback_query.register(setting, F.data == "Настройки")
