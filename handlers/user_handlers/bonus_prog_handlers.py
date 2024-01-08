from aiogram import types, Dispatcher, F
from aiogram.filters import CommandStart

from data.database.function import getBalance
from keyboards.user_kb import main_kb, galery_kb, aboutUs_kb, bonus_kb, services_kb





async def conditions(callback: types.CallbackQuery):
    await callback.message.delete()
    await callback.message.answer(f"Очень важные условия\n1. Спам - бан\n2. Скам - бан")
    await callback.message.answer(f"Бонусная программа", reply_markup=bonus_kb())

async def participate(callback: types.CallbackQuery):
    await callback.message.delete()
    await callback.message.answer(f"Теперь выучавствуете")
    await callback.message.answer(f"Бонусная программа", reply_markup=bonus_kb())





def register_bonus_user_handlers(dp: Dispatcher):
    dp.callback_query.register(conditions, F.data == "Условия")
    dp.callback_query.register(participate, F.data == "Учавствовать")
