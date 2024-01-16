import datetime

from aiogram import types, Dispatcher, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from data.config import password
from keyboards.admin_kb import main_admin_kb, cancel_kb
from keyboards.user_kb import main_kb
from utils.states import CheckAdminState
import datetime


async def start(message: types.Message, state: FSMContext):
    await message.answer(f"Введите пароль для доступа к админ панели", reply_markup=cancel_kb())
    await state.set_state(CheckAdminState.password)


class ab:
    tryes = 5
    last_try = datetime.datetime.now()
async def checkAdmin(message: types.Message, state: FSMContext):
    if (message.text == "Отмена"):
        await state.clear()
        await message.answer(f"Главная", reply_markup=main_kb())
    else:
        if (ab.tryes == 1):
            ab.tryes -= 1
            ab.last_try = datetime.datetime.now()

        elif (datetime.datetime.now() > ab.last_try + datetime.timedelta(minutes=1)):
            ab.tryes = 5

        elif (ab.tryes > 0 and message.text == password):
            await message.answer(f"Главная (админка)", reply_markup=main_admin_kb())
            await state.clear()
        else:
            if(ab.tryes<0):
                ab.tryes -= 1
                await message.answer(f"Подождите пять минут")
            else:
                ab.tryes -= 1
                await message.answer(f"Неверный пароль")




async def back(callback: types.CallbackQuery):
    await callback.message.edit_text(f"Главная (админка)", reply_markup=main_admin_kb())


def register_main_admin_handlers(dp: Dispatcher):
    dp.message.register(start, Command(commands=['admin']))
    dp.message.register(checkAdmin, CheckAdminState.password)
    dp.callback_query.register(back, F.data == "Назад_admin")
