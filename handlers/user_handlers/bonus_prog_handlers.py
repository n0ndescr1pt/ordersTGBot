import json

from aiogram import types, Dispatcher, F
from keyboards.user_kb import bonus_kb





async def conditions(callback: types.CallbackQuery):
    await callback.message.delete()
    with open("data/feed.json", "r", encoding='utf-8') as f:
        data = json.load(f)
    await callback.message.answer(f"{data['bonus_prog']['condition']}")
    await callback.message.answer(f"Бонусная программа", reply_markup=bonus_kb())

async def participate(callback: types.CallbackQuery):
    await callback.message.delete()
    await callback.message.answer(f"Теперь выучавствуете")
    await callback.message.answer(f"Бонусная программа", reply_markup=bonus_kb())





def register_bonus_user_handlers(dp: Dispatcher):
    dp.callback_query.register(conditions, F.data == "Условия")
    dp.callback_query.register(participate, F.data == "Учавствовать")
