import datetime

from aiogram import types, Dispatcher, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from data.config import password
from data.database.function import getUserIDfromNickname
from keyboards.admin_kb import main_admin_kb, cancel_kb
from keyboards.user_kb import main_kb
from utils.states import CheckAdminState, SendMessageToUserState
import datetime




async def start(message: types.Message, state: FSMContext):
    class Password:
        def __init__(self, attemp, last_try, count_try):
            """Constructor"""
            self.attemp = attemp
            self.last_try = last_try
            self.count_try = count_try
    await state.update_data(attemps=Password(attemp=5,last_try=None, count_try=0))

    await message.answer(f"Введите пароль для доступа к админ панели", reply_markup=cancel_kb())
    await state.set_state(CheckAdminState.password)



async def checkAdmin(message: types.Message, state: FSMContext):
    data = await state.get_data()
    if (message.text == "Отмена"):
        await state.clear()
        await message.answer(f"Главная", reply_markup=main_kb())
    else:
        if(message.text == password):
            await message.answer(f"Главная (админка)", reply_markup=main_admin_kb())
            await state.clear()
        else:
            data['attemps'].attemp-=1
            await message.answer(f"Неверный пароль, осталось {data['attemps'].attemp} попытки")
            if (data['attemps'].attemp<=1):
                data['attemps'].count_try +=1
                data['attemps'].last_try = datetime.datetime.now()
                await state.set_state(CheckAdminState.wrongPassword)

async def wrongPass(message: types.Message, state: FSMContext):
    data = await state.get_data()
    if (message.text == "Отмена"):
        await state.clear()
        await message.answer(f"Главная", reply_markup=main_kb())
    else:
        time = {"1":0.30,"2":1,"3":5,"4":10}
        cooldown = time[f"{data['attemps'].count_try}"]
        if (datetime.datetime.now() > data['attemps'].last_try + datetime.timedelta(minutes=cooldown)):
            if (message.text == password):
                await message.answer(f"Главная (админка)", reply_markup=main_admin_kb())
                await state.clear()
            else:
                data['attemps'].attemp = 5
                await message.answer(f"Неверный пароль", reply_markup=cancel_kb())
                await state.set_state(CheckAdminState.password)
        else:
            await message.answer(f"Подождите {round(((data['attemps'].last_try + datetime.timedelta(minutes=cooldown) - datetime.datetime.now()).seconds)/60,2)} минут перед следующей попыткой")


async def sendMessageToUser(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer(f"Введите никнейм пользователя (@nickname)")
    await state.set_state(SendMessageToUserState.getUsername)

async def getMessageToUser(message: types.Message, state: FSMContext):
    if (message.text == "Отмена"):
        await state.clear()
        await message.answer(f"Главная (админка)", reply_markup=main_admin_kb())
    else:
        user_id = await getUserIDfromNickname(message.text)
        if (user_id is not None):
            await state.update_data(nickname=message.text)
            await message.answer(f"Введите сообщение, которое хотите отправить этому пользователю")
            await state.set_state(SendMessageToUserState.getMessage)
        else:
            await message.answer(f"Неверное имя пользователя, попробуйте еще раз")
            await message.answer(f"Введите никнейм пользователя (@nickname)")


async def sendMessage(message: types.Message, state: FSMContext):
    if (message.text == "Отмена"):
        await state.clear()
        await message.answer(f"Главная", reply_markup=main_kb())
    else:
        data = await state.get_data()
        user_id = await getUserIDfromNickname(data['nickname'])
        await message.bot.send_message(user_id[0],text=message.text)
        await message.answer(f"Сообщение успешно отправлено")
        await message.answer(f"Главная (админка)", reply_markup=main_admin_kb())


async def back(callback: types.CallbackQuery):
    await callback.message.edit_text(f"Главная (админка)", reply_markup=main_admin_kb())





def register_main_admin_handlers(dp: Dispatcher):
    dp.message.register(start, Command(commands=['admin']))
    dp.message.register(checkAdmin, CheckAdminState.password)
    dp.callback_query.register(back, F.data == "Назад_admin")
    dp.message.register(wrongPass,CheckAdminState.wrongPassword)

    dp.callback_query.register(sendMessageToUser, F.data == "sendMessageToUser")
    dp.message.register(getMessageToUser,SendMessageToUserState.getUsername)
    dp.message.register(sendMessage, SendMessageToUserState.getMessage)