from aiogram import types, Dispatcher, F
from aiogram.filters import CommandStart


from keyboards.user_kb import main_kb, galery_kb, aboutUs_kb, bonus_kb, services_kb




async def priceList(callback: types.CallbackQuery):
    await callback.message.delete()
    await callback.message.answer(f"Ваш баланс 7\\-8 рублей создать бд повзязать баланс")
    await callback.message.answer(f"Услуги", reply_markup=services_kb())


async def supportAdmin(callback: types.CallbackQuery):
    await callback.message.delete()
    await callback.message.answer(f"Очень важные условия")
    await callback.message.answer(f"Услуги", reply_markup=services_kb())


async def order(callback: types.CallbackQuery):
    await callback.message.delete()
    await callback.message.answer(f"Бесполезная кнопка")
    await callback.message.answer(f"Услуги", reply_markup=services_kb())


async def preOrder(callback: types.CallbackQuery):
    await callback.message.delete()
    await callback.message.answer(f"Бесполезная кнопка")
    await callback.message.answer(f"Услуги", reply_markup=services_kb())


def register_services_user_handlers(dp: Dispatcher):
    dp.callback_query.register(priceList, F.data == "Прайс лист")
    dp.callback_query.register(supportAdmin, F.data == "Связь со спецом")
    dp.callback_query.register(order, F.data == "Оформить заказ")
    dp.callback_query.register(preOrder, F.data == "Предварительный расчет")
