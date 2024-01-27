import json
import re

from aiogram import types, Dispatcher, F
from aiogram.enums import InputMediaType

from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile
from aiogram.utils.media_group import MediaGroupBuilder

from data.config import Admin, chat
from data.database.function import getBalance, insertOrder, insertOrderWithCalc, getUserPhoneAndName, setUserPhoneAndName
from keyboards.admin_kb import confirm_order_kb, calculate_order_kb
from keyboards.user_kb import services_kb, yesNo_kb, getPhone_kb, ready_kb
from utils.callbackFactory import NumbersCallbackFactoryConfirmOrder, NumbersCallbackFactorySetOrderUsPaid, \
    NumbersCallbackFactoryDeleteOrder, NumbersCallbackFactorySetOrderAsReadyToSend
from utils.someMethods import cancelCalcOrder
from utils.states import OrderState, ConfirmOrderState


async def priceList(callback: types.CallbackQuery):
    await callback.message.delete()

    document = FSInputFile('data/prices.xlsx')
    await callback.message.answer_document(document)
    await callback.message.answer(f"(не является публичной оффертой)")
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
        phone = await getUserPhoneAndName(callback.from_user.id)

        if(phone[0] == None):
            await callback.message.answer(f"Для удобной связи нужен ваш телефон", reply_markup=getPhone_kb())
            await state.set_state(OrderState.getPhone)
        else:
            docsId = []
            await state.update_data(docs=docsId)
            await callback.message.answer(f"K заказу будет прикреплен ваш номер телефона")
            await callback.message.answer(f"Введите ваш email")
            await state.set_state(OrderState.getEmail)


async def getPhone(message: types.Message, state: FSMContext):
    if (message.text == "Отмена"):
        await cancelCalcOrder(message, state)
    else:
        docsId = []
        await state.update_data(docs=docsId)
        await state.update_data(phone=message.contact.phone_number)
        await setUserPhoneAndName(user_id=message.from_user.id, phone=message.contact.phone_number,first_name=message.contact.first_name)
        await state.update_data(name=message.contact.first_name)
        await message.answer(f"Введите ваш email")
        await state.set_state(OrderState.getEmail)

async def getEmail(message: types.Message, state: FSMContext):
    if (message.text == "Отмена"):
        await cancelCalcOrder(message, state)
    else:
        regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
        if re.fullmatch(regex, message.text):
            await state.update_data(email=message.text)
            balance = await getBalance(message.from_user.id)
            await message.answer(f"У вас {round(balance[0],2)} бонусов, списываем бонусы?", reply_markup=yesNo_kb())
            await state.set_state(OrderState.setBonus)
        else:
            await message.answer(f"Введен некорректный email")



async def setBonus(message: types.Message, state: FSMContext):
    if (message.text == "Отмена"):
        await cancelCalcOrder(message, state)
    else:
        contact = await getUserPhoneAndName(message.from_user.id)
        await state.update_data(phone=contact[0])
        await state.update_data(name=contact[1])

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



async def addFile(message: types.Message, state: FSMContext):
    data = await state.get_data()

    if(message.text=="Отмена"):
        await cancelCalcOrder(message, state)

    elif(message.text=="Готово"):
        bonusBalance = data['setBonus']
        user_id = message.from_user.id
        name = data['name']
        phone = data['phone']
        dumpsDocsId = json.dumps(data['docs'])
        email = data['email']
        try:
            countPacks = data['countPack']
            volume = data['volume']
            needPurchase = data['needPurchase']
            ratio = data['type']
            final = data['final']

            orderID = await insertOrderWithCalc(user_id, bonusBalance, name, phone, dumpsDocsId, countPacks, volume, needPurchase ,ratio,final,"unconfirmed",email)

            await message.bot.send_message(chat_id=chat,
                                               text=f"пользователь с ником @{message.from_user.username} оформил заказ с калькуляцией на {final} рублей, "
                                                    f"\nНомер телефона: {phone}"
                                                    f"\nemail: {email}"
                                                    f"\nИмя: {name}"
                                                    f"\nСписанные бонусы: {bonusBalance}"
                                                    f"\nКоличество упаковок: {countPacks}"
                                                    f"\nОбъем: {volume}"
                                                    f"\nНеобходима ли закупка: {needPurchase}"
                                                    f"\nКоэффицент: {ratio}"
                                                    f"\nid заказа: {orderID}")


            album_builder = MediaGroupBuilder(
                caption=f"Документы к заказу"
            )
            if (len(data['docs']) > 0):
                for doc in data['docs']:
                    album_builder.add(type=InputMediaType.DOCUMENT, media=doc)
                await message.bot.send_media_group(chat_id=chat, media=album_builder.build())
            await message.bot.send_message(chat_id=chat,
                                           text=f"Для подтверждения заказа нажмите на кнопку",
                                           reply_markup= await calculate_order_kb(orderID))


        except KeyError:
            orderID = await insertOrder(user_id, bonusBalance, name, phone, dumpsDocsId, "unconfirmed",email)



            await message.bot.send_message(chat_id=chat,
                                           text=f"пользователь с ником @{message.from_user.username} оформил заказ, "
                                                f"\nНомер телефона: {phone}"
                                                f"\nemail: {email}"
                                                f"\nИмя: {name}"
                                                f"\nСписанные бонусы: {bonusBalance}"
                                                f"\nid заказа: {orderID}")
            album_builder = MediaGroupBuilder(
                caption=f"Документы к заказу"
            )
            if(len(data['docs']) > 0):
                for doc in data['docs']:
                    album_builder.add(type=InputMediaType.DOCUMENT, media=doc)
                await message.bot.send_media_group(chat_id=chat, media=album_builder.build())
            await message.bot.send_message(chat_id=chat,
                                           text=f"Для подтверждения заказа нажмите на кнопку", reply_markup= await calculate_order_kb(orderID))



        await state.clear()
        await message.answer(f"В ближайшее время с вами свяжется специалист")

        await message.answer(f"Услуги", reply_markup=services_kb())
    else:
        data['docs'].append(message.document.file_id)
        await message.answer(f"Можете отправить еще один файл",reply_markup=ready_kb())


def register_services_user_handlers(dp: Dispatcher):
    dp.callback_query.register(priceList, F.data == "Прайс лист")
    dp.callback_query.register(supportAdmin, F.data == "Связь со спецом")
    dp.callback_query.register(order, F.data == "Оформить заказ")

    dp.message.register(getPhone, OrderState.getPhone)
    dp.message.register(setBonus, OrderState.setBonus)
    dp.message.register(countBonus, OrderState.countBonus)
    dp.message.register(addFile, OrderState.addFile)
    dp.message.register(getEmail, OrderState.getEmail)
