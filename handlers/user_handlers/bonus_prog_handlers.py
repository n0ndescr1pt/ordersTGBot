from aiogram import types, Dispatcher, F
from aiogram.filters import CommandStart


from keyboards.user_kb import main_kb, galery_kb, aboutUs_kb, bonus_kb, services_kb




async def balance(callback: types.CallbackQuery):
    await callback.message.delete()
    await callback.message.answer(f"Ваш баланс 7\\-8 рублей создать бд повзязать баланс")
    await callback.message.answer(f"Бонусная программа", reply_markup=bonus_kb())

async def conditions(callback: types.CallbackQuery):
    await callback.message.delete()
    await callback.message.answer(f"Очень важные условия")
    await callback.message.answer(f"Бонусная программа", reply_markup=bonus_kb())

async def participate(callback: types.CallbackQuery):
    await callback.message.delete()
    await callback.message.answer(f"Бесполезная кнопка")
    await callback.message.answer(f"Бонусная программа", reply_markup=bonus_kb())





def register_bonus_user_handlers(dp: Dispatcher):
    dp.callback_query.register(balance, F.data == "Баланс")
    dp.callback_query.register(conditions, F.data == "Условия")
    dp.callback_query.register(participate, F.data == "Учавствовать")
