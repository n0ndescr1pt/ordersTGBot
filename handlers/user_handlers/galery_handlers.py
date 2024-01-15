
from aiogram import types, Dispatcher, F

from keyboards.user_kb import galery_kb
from utils.someMethods import getGaleryItems


async def marketplaces(callback: types.CallbackQuery):
    await callback.message.delete()
    await getGaleryItems(callback.message, "marketplace","Маркетплейс")
    await callback.message.answer(f"Галерея", reply_markup=galery_kb())

async def presents(callback: types.CallbackQuery):
    await callback.message.delete()
    await getGaleryItems(callback.message, "present","Подарки")
    await callback.message.answer(f"Галерея", reply_markup=galery_kb())

async def individualYpakovka(callback: types.CallbackQuery):
    await callback.message.delete()
    await getGaleryItems(callback.message, "individualPack","Индивидиульная упаковка")
    await callback.message.answer(f"Галерея", reply_markup=galery_kb())

async def fullfillment(callback: types.CallbackQuery):
    await callback.message.delete()
    await getGaleryItems(callback.message,"fullfillment","Фуллфиллмент")
    await callback.message.answer(f"Галерея", reply_markup=galery_kb())






def register_galery_user_handlers(dp: Dispatcher):
    dp.callback_query.register(marketplaces, F.data == "Маркетплейсы")
    dp.callback_query.register(presents, F.data == "Подарки")
    dp.callback_query.register(individualYpakovka, F.data == "Индивидуальная упаковка")
    dp.callback_query.register(fullfillment, F.data == "Фулфилмент")
