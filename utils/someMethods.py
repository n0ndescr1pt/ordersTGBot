from aiogram import types
from aiogram.fsm.context import FSMContext

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