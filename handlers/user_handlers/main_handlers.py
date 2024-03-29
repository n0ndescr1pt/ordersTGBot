from aiogram import types, Dispatcher, F
from aiogram.filters import CommandStart

from data.database.function import addUser, getBalance
from keyboards.user_kb import main_kb, galery_kb, aboutUs_kb, bonus_kb, services_kb


async def start(message: types.Message):
    await message.answer(f"Главная", reply_markup=main_kb())
    addUser(message.from_user.id,message.from_user.username)



async def galery(callback: types.CallbackQuery):
    await callback.message.edit_text(f"<b><em>Галерея</em></b>", reply_markup=galery_kb())


async def aboutUs(callback: types.CallbackQuery):
    await callback.message.edit_text(f"О нас", reply_markup=aboutUs_kb())

async def bonus(callback: types.CallbackQuery):
    balance = await getBalance(callback.from_user.id)
    await callback.message.edit_text(f"Бонусная программа\nВаш бонусный баланс = {balance[0]}", reply_markup=bonus_kb())

async def services(callback: types.CallbackQuery):
    await callback.message.edit_text(f"Услуги", reply_markup=services_kb())

async def back(callback: types.CallbackQuery):
    await callback.message.edit_text(f"Главная", reply_markup=main_kb())







def register_main_user_handlers(dp: Dispatcher):
    dp.message.register(start, CommandStart())
    dp.callback_query.register(galery, F.data == "Галерея")
    dp.callback_query.register(aboutUs, F.data == "О нас")
    dp.callback_query.register(bonus, F.data == "Бонусная программа")
    dp.callback_query.register(services, F.data == "Услуги")
    dp.callback_query.register(back, F.data == "Назад")