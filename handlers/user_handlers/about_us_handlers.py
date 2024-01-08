from aiogram import types, Dispatcher, F
from aiogram.filters import CommandStart


from keyboards.user_kb import main_kb, galery_kb, aboutUs_kb, bonus_kb, services_kb




async def aboutCompany(callback: types.CallbackQuery):
    await callback.message.delete()
    await callback.message.answer(f"Это очень классная компания вставьте тут свой текст")
    await callback.message.answer(f"О нас", reply_markup=aboutUs_kb())


async def judicialInf(callback: types.CallbackQuery):
    await callback.message.delete()
    await callback.message.answer(f"Очень важная юридическая информация")
    await callback.message.answer(f"О нас", reply_markup=aboutUs_kb())



def register_aboutUs_user_handlers(dp: Dispatcher):
    dp.callback_query.register(aboutCompany, F.data == "О компании")
    dp.callback_query.register(judicialInf, F.data == "Юридическая информация")
