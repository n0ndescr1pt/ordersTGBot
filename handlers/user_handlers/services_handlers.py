import json

from aiogram import types, Dispatcher, F

from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile
from aiogram import Bot
from data.config import Admin
from data.database.function import getBalance, insertOrder
from keyboards.admin_kb import cancel_kb
from keyboards.user_kb import main_kb, galery_kb, aboutUs_kb, bonus_kb, services_kb, yesNo_kb, do_order_kb, getPhone_kb, \
    ready_kb
from utils.someMethods import cancelCalcOrder
from utils.states import PreOrderState, OrderState


async def priceList(callback: types.CallbackQuery):
    await callback.message.delete()

    document = FSInputFile('data/prices.xlsx')
    await callback.message.answer_document(document)
    await callback.message.answer(f"Услуги", reply_markup=services_kb())


async def supportAdmin(callback: types.CallbackQuery):
    await callback.message.delete()
    await callback.message.answer(f"В ближайшее время с вами свяжется специалист")
    for admin in Admin:
        await callback.bot.send_message(chat_id=admin,text=f"пользователь с ником @{callback.from_user.username} хочет связаться со специалистом")
    await callback.message.answer(f"Услуги", reply_markup=services_kb())


async def order(callback: types.CallbackQuery, state: FSMContext):
    if (callback.message.text == "Отмена"):
        await cancelCalcOrder(callback.message, state)
    else:
        await callback.message.delete()
        await callback.message.answer(f"Для удобной связи нужен ваш телефон", reply_markup=getPhone_kb())
        #await bot.send_photo(chat_id=callback.message.chat.id, photo=a)
        await state.set_state(OrderState.getPhone)

async def getPhone(message: types.Message, state: FSMContext):
    await state.update_data(phone=message.contact.phone_number)
    await state.update_data(name=message.contact.first_name)
    balance = await getBalance(message.from_user.id)
    await message.answer(f"У вас {balance[0]} бонусов, списываем бонусы?", reply_markup=yesNo_kb())
    await state.set_state(OrderState.setBonus)

async def setBonus(message: types.Message, state: FSMContext):
    if (message.text == "Отмена"):
        await cancelCalcOrder(message, state)
    else:
        if(message.text == "Да"):
            await message.answer(f"Введите сумму")
            await state.set_state(OrderState.countBonus)
        elif(message.text == "Нет"):
            await state.update_data(setBonus=0)
            await message.answer(f"Прикрепите файлы (ТЗ, пожелания)",reply_markup=ready_kb())
            await state.set_state(OrderState.addFile)
        else:
            await message.answer(f"Ответье да или нет")

async def countBonus(message: types.Message, state: FSMContext):
    if (message.text == "Отмена"):
        await cancelCalcOrder(message, state)
    else:
        try:
            user_balance = await getBalance(message.from_user.id)
            if (float(message.text) > user_balance[0]):
                await message.answer(f"Введите сумму соответствующее вашему балансу")
            else:
                await state.update_data(setBonus=int(message.text))
                await message.answer(f"Прикрепите файлы (ТЗ, пожелания)",reply_markup=ready_kb())
                await state.set_state(OrderState.addFile)
        except ValueError:
            await message.answer(f"Вводите число")


docsId = []
async def addFile(message: types.Message, state: FSMContext):
    if(message.text=="Отмена"):
        await cancelCalcOrder(message, state)
        docsId.clear()

    elif(message.text=="Готово"):
        data = await state.get_data()
        bonusBalance = data['setBonus']
        user_id = message.from_user.id
        name = data['name']
        phone = data['phone']
        dumpsDocsId = json.dumps(docsId)
        await insertOrder(user_id,bonusBalance, name, phone, dumpsDocsId)
        docsId.clear()
        await state.clear()
        await message.answer(f"В ближайшее время с вами свяжется специалист")
        await message.answer(f"Услуги", reply_markup=services_kb())
    else:
        docsId.append(message.document.file_id)
        print(docsId)
        await message.answer(f"Можете отправить еще один файл",reply_markup=ready_kb())




#предварительный расчет
async def preOrder(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer(f"Для расчета приблизительной стоимости введите количество упаковок", reply_markup=cancel_kb())
    await state.set_state(PreOrderState.countPack)

async def calcCount(message: types.Message, state: FSMContext):
    try:
        if (message.text == "Отмена"):
            await cancelCalcOrder(message, state)
        else:
            await state.update_data(countPack=int(message.text))
            await message.answer(f"Введите Длинну Ширину Высоту (через пробел в сантиметрах)", reply_markup=cancel_kb())
            await state.set_state(PreOrderState.volume)
    except ValueError:
        await message.answer(f"Введите целое число")

async def calcVolume(message: types.Message, state: FSMContext):
    if (message.text == "Отмена"):
        await cancelCalcOrder(message, state)
    else:
        volume = message.text.split(' ')
        #проверка правильно ли пользователь ввел длину ширину и высоту
        if(len(volume) == 3 and volume[0].isdigit() and volume[1].isdigit() and volume[2].isdigit()):
            await state.update_data(volume=message.text)
            await message.answer(f"Необходима ли закупка", reply_markup=yesNo_kb())
            await state.set_state(PreOrderState.needPurchase)
        else:
            await message.answer(f"Введите Длинну Ширину Высоту (через пробел в сантиметрах)")

async def calcNeedPurchapse(message: types.Message, state: FSMContext):
    if (message.text == "Отмена"):
        await cancelCalcOrder(message, state)
    else:
        if(message.text == "Да" or message.text == "Нет"):
            await state.update_data(needPurchase=message.text)
            await message.answer(f"Введите Тип (коэффицент)")
            await state.set_state(PreOrderState.type)
        else:
            await message.answer(f"Ответье да или нет")

async def calcType(message: types.Message, state: FSMContext):
    try:
        await state.update_data(type=float(message.text))
        data = await state.get_data()
        volume = data['volume'].split(' ')
        final = (( int(volume[0]) * int(volume[1]) * int(volume[2]) + int(volume[0]) * int(volume[1]) * int(volume[2]) * 0.3) * data['type']) * data['countPack'] #расчет стоимости
        await message.answer(f"Приблизительная цена партии будет составлять {final} рублей")

        #добавить сообщение админу
        for admin in Admin:
            await message.bot.send_message(chat_id=admin, text=f"пользователь с ником @{message.from_user.username} осуществил калькуляцию на {final} рублей")

        await state.clear()
        await message.answer(f"Оформить заказ?",reply_markup=do_order_kb())

    except ValueError:
        await message.answer(f"Введите Тип (коэффицент) числом")


async def no(callback: types.CallbackQuery):
    await callback.message.delete()
    await callback.message.answer(f"Услуги", reply_markup=services_kb())

async def yes(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer(f"Для удобной связи нужен ваш телефон", reply_markup=getPhone_kb())
    # await bot.send_photo(chat_id=callback.message.chat.id, photo=a)
    await state.set_state(OrderState.getPhone)

#конец предварительного расчета


def register_services_user_handlers(dp: Dispatcher):
    dp.callback_query.register(priceList, F.data == "Прайс лист")
    dp.callback_query.register(supportAdmin, F.data == "Связь со спецом")
    dp.callback_query.register(order, F.data == "Оформить заказ")
    dp.callback_query.register(preOrder, F.data == "Предварительный расчет", StateFilter(None))

    dp.message.register(calcCount, PreOrderState.countPack)
    dp.message.register(calcVolume, PreOrderState.volume)
    dp.message.register(calcNeedPurchapse, PreOrderState.needPurchase)
    dp.message.register(calcType, PreOrderState.type)

    dp.callback_query.register(no, F.data == "Нет")
    dp.callback_query.register(yes, F.data == "Да")

    dp.message.register(getPhone, OrderState.getPhone)
    dp.message.register(setBonus, OrderState.setBonus)
    dp.message.register(countBonus, OrderState.countBonus)
    dp.message.register(addFile, OrderState.addFile)