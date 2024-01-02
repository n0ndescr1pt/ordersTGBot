import time

from aiogram import types, Dispatcher, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from data.config import password
from keyboards.admin_kb import main_admin_kb, cancel_kb
from keyboards.user_kb import main_kb
from states import CheckAdmin


async def start(message: types.Message, state:FSMContext):
    pass







def register_upload_stat_admin_handlers(dp: Dispatcher):
    dp.message.register(start, Command(commands=['admin']))
