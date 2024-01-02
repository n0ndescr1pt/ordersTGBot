import time

from aiogram import types, Dispatcher, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from data.config import password
from keyboards.admin_kb import main_admin_kb, cancel_kb, settings_kb, edit_galery_kb
from keyboards.user_kb import main_kb
from states import CheckAdmin


async def edit_galery(callback: types.CallbackQuery):
    await callback.message.edit_text(f"Редактировать галареи", reply_markup=edit_galery_kb())









def register_edit_galery_admin_handlers(dp: Dispatcher):
    dp.callback_query.register(edit_galery, F.data == "Редактировать галереи")
