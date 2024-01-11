import re

from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.utils.media_group import MediaGroupBuilder

from data.database.function import selectGalery
from keyboards.admin_kb import settings_kb, edit_galery_kb
from keyboards.user_kb import services_kb


async def cancelCalcOrder(message: types.Message, state:FSMContext):
    await state.clear()
    await message.answer(text=f"Действие отменено")
    await message.answer(text=f"Услуги", reply_markup=services_kb())

async def cancelUpdatePriceList(message: types.Message, state:FSMContext):
    await state.clear()
    await message.answer(text=f"Действие отменено")
    await message.answer(text=f"Настройки", reply_markup=settings_kb())

async def cancelEditGalery(message: types.Message, state:FSMContext):
    await state.clear()
    await message.answer(text=f"Действие отменено")
    await message.answer(f"Редактировать галареи", reply_markup=edit_galery_kb())

async def getGaleryItems(message: types.Message,galery_id):
    galeryItems = await selectGalery(galery_id)

    for item in galeryItems:
        list_img = re.findall(r'\"(.*?)\"', item[2])
        album_builder = MediaGroupBuilder(
            caption=item[3]
        )
        for img in list_img:
            album_builder.add(type="photo", media=img)

        await message.answer_media_group(media=album_builder.build())