from aiogram import types, Dispatcher, F
from aiogram.client import bot
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from keyboards.admin_kb import settings_kb
from utils.someMethods import cancelUpdatePriceList
from utils.states import UpdatePriceListState


async def setting(callback: types.CallbackQuery):
    await callback.message.edit_text(f"Настройки", reply_markup=settings_kb())


async def updatePriceList(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer(f"Отправьте прайс лист")
    await state.set_state(UpdatePriceListState.updatePriceList)

async def uploadPriceList(message: types.Message, state:FSMContext):
    if (message.text == "Отмена"):
        await cancelUpdatePriceList(message, state)
    else:
        document = message.document
        await message.bot.download(file=document, destination="data/prices.xlsx")

        await message.answer(f"Прайс лист успешно обновлен")
        await message.answer(f"Настройки", reply_markup=settings_kb())
        await state.clear()

def register_settings_admin_handlers(dp: Dispatcher):
    dp.callback_query.register(setting, F.data == "Настройки")
    dp.callback_query.register(updatePriceList, F.data == "обновитьПрайсЛист")
    dp.message.register(uploadPriceList, UpdatePriceListState.updatePriceList)

