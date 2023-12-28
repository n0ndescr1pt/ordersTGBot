from aiogram import types, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import FSInputFile
from aiogram.utils.media_group import MediaGroupBuilder

from keyboards.user_kb import main_kb, galery_kb, aboutUs_kb, bonus_kb, services_kb




async def marketplaces(callback: types.CallbackQuery):
    await callback.message.delete()

    media_group = MediaGroupBuilder(caption="Media group caption")

    media_group.add(type="photo", media=FSInputFile("assets/1.png"))
    media_group.add(type="photo", media=FSInputFile("assets/1.png"))
    media_group.add(type="photo", media=FSInputFile("assets/1.png"))

    await callback.message.answer_media_group(media=media_group.build())

    await callback.message.answer(f"Галерея", reply_markup=galery_kb())

async def presents(callback: types.CallbackQuery):
    pass

async def individualYpakovka(callback: types.CallbackQuery):
    pass

async def fullfillment(callback: types.CallbackQuery):
    pass






def register_galery_user_handlers(dp: Dispatcher):
    dp.callback_query.register(marketplaces, F.data == "Маркетплейсы")
    dp.callback_query.register(presents, F.data == "Подарки")
    dp.callback_query.register(individualYpakovka, F.data == "Индивидуальная упаковка")
    dp.callback_query.register(fullfillment, F.data == "Фулфилмент")
