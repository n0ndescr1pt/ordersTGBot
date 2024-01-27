from aiogram import Dispatcher, F, types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from data.config import Admin
from keyboards.admin_kb import cancel_kb
from keyboards.user_kb import services_kb, getPhone_kb, do_order_kb, yesNo_kb, get_coefficient_kb
from utils.callbackFactory import CoefficientPreOrder
from utils.someMethods import cancelCalcOrder
from utils.states import PreOrderState, OrderState


async def preOrder(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer(f"Для расчета приблизительной стоимости введите количество (штук)", reply_markup=cancel_kb())
    await state.set_state(PreOrderState.countPack)

async def calcCount(message: types.Message, state: FSMContext):
    try:
        if (message.text == "Отмена"):
            await cancelCalcOrder(message, state)
        else:
            await state.update_data(countPack=int(message.text))
            await message.answer(f"Введите Длину Ширину Высоту (пример 3 3 3)", reply_markup=cancel_kb())
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
            await message.answer(f"Введите Тип (коэффицент)",reply_markup=get_coefficient_kb())
            await state.set_state(PreOrderState.type)
        else:
            await message.answer(f"Ответье да или нет")

async def calcType(callback: types.CallbackQuery, state: FSMContext,callback_data: CoefficientPreOrder):
    await callback.message.delete()
    try:
        await state.update_data(type=callback_data.coefficient)
        data = await state.get_data()
        volume = data['volume'].split(' ')
        final = (( int(volume[0]) * int(volume[1]) * int(volume[2]) + int(volume[0]) * int(volume[1]) * int(volume[2]) * 0.3) * data['type']) * data['countPack'] #расчет стоимости
        await state.update_data(final=final)
        await callback.message.answer(f"Приблизительная цена партии будет составлять {round(final,2)} рублей")

        #добавить сообщение админу
        for admin in Admin:
            await callback.bot.send_message(chat_id=admin, text=f"пользователь с ником @{callback.message.from_user.username} осуществил калькуляцию на {round(final,2)} рублей")

        await callback.message.answer(f"Оформить заказ?",reply_markup=do_order_kb())

    except ValueError:
        await callback.message.answer(f"Введите Тип (коэффицент) числом")


async def no(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.clear()
    await callback.message.answer(f"Услуги", reply_markup=services_kb())

async def yes(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()

    await callback.message.answer(f"Для удобной связи нужен ваш телефон", reply_markup=getPhone_kb())
    await state.set_state(OrderState.getPhone)



def register_services_preOrder_user_handlers(dp: Dispatcher):
    dp.callback_query.register(preOrder, F.data == "Предварительный расчет", StateFilter(None))

    dp.message.register(calcCount, PreOrderState.countPack)
    dp.message.register(calcVolume, PreOrderState.volume)
    dp.message.register(calcNeedPurchapse, PreOrderState.needPurchase)
    dp.callback_query.register(calcType, CoefficientPreOrder.filter())

    dp.callback_query.register(no, F.data == "Нет")
    dp.callback_query.register(yes, F.data == "Да")