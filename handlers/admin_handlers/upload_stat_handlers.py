from aiogram import types, Dispatcher
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext


async def start(message: types.Message, state:FSMContext):
    pass







def register_upload_stat_admin_handlers(dp: Dispatcher):
    dp.message.register(start, Command(commands=['admin']))
