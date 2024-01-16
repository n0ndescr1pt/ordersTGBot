import json

from aiogram import types, Dispatcher, F
from aiogram.filters import CommandStart


from keyboards.user_kb import main_kb, galery_kb, aboutUs_kb, bonus_kb, services_kb




async def aboutCompany(callback: types.CallbackQuery):
    await callback.message.delete()
    with open("data/feed.json","r", encoding='utf-8') as f:
        data = json.load(f)
    await callback.message.answer(f"{data['about_us']['about_company']}")
    await callback.message.answer(f"О нас", reply_markup=aboutUs_kb())


async def judicialInf(callback: types.CallbackQuery):
    await callback.message.delete()
    with open("data/feed.json","r", encoding='utf-8') as f:
        data = json.load(f)
    await callback.message.answer(f"{data['about_us']['judicial_info']}")
    await callback.message.answer(f"О нас", reply_markup=aboutUs_kb())



def register_aboutUs_user_handlers(dp: Dispatcher):
    dp.callback_query.register(aboutCompany, F.data == "О компании")
    dp.callback_query.register(judicialInf, F.data == "Юридическая информация")
