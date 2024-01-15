from aiogram import types, Dispatcher, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from data.database.function import confirmOrderPaid, confirmOrderStatus, deleteOrderFromDB, getOrderStatus
from keyboards.admin_kb import cancel_kb, main_admin_kb
from keyboards.user_kb import confirmOrder_kb
from utils.someMethods import cancelConfirmOrder
from utils.states import ConfirmOrderByIDState


async def confirmOrder(callback: types.CallbackQuery, state:FSMContext):
    if (callback.message.text == "Отмена"):
        await cancelConfirmOrder(callback.message, state)
    else:
        await callback.message.answer(f"Введите id заказа")
        await state.set_state(ConfirmOrderByIDState.getOrderID)


async def confirmOrderSumm(message: types.Message, state: FSMContext):
    if (message.text == "Отмена"):
        await cancelConfirmOrder(message, state)
    else:
            await state.update_data(orderID=message.text)
            await message.answer(f"Какое действие", reply_markup=confirmOrder_kb())
            await state.set_state(ConfirmOrderByIDState.confirmOrder)


async def confirmOrderByID(message: types.Message, state: FSMContext):
    if (message.text == "Отмена"):
        await cancelConfirmOrder(message, state)
    elif(message.text == "Подтвердить"):
        await message.answer(f"Введите сумму за этот заказ", reply_markup=cancel_kb())
        await state.set_state(ConfirmOrderByIDState.setSumm)
    elif (message.text == "Отметить как оплачено"):
        data = await state.get_data()
        order_id = data['orderID']
        order_status = await getOrderStatus(order_id)
        if (order_status[0] != "confirm"):
            await message.answer(f"Сначала подтвердите заказ")
            await state.clear()
        else:

            user_id = await confirmOrderPaid(order_id, "paid")
            await message.answer(f"Заказ {order_id} отмечен как оплачен")
            await message.answer(text=f"Главная (админка)", reply_markup=main_admin_kb())
            await message.bot.send_message(chat_id=user_id[0],
                                        text=f"Оплата заказа подтверждена, заказ находится в обработке")
    elif (message.text == "Удалить"):
        data = await state.get_data()
        order_id = data['orderID']
        await deleteOrderFromDB(order_id=order_id)
        await message.answer(f"Заказ {order_id} удален")
        await message.answer(text=f"Главная (админка)", reply_markup=main_admin_kb())


async def setOrderSumm(message: types.Message, state: FSMContext):
    if (message.text == "Отмена"):
        await cancelConfirmOrder(message, state)
    else:
        try:
            await state.update_data(orderSumm=message.text)
            data = await state.get_data()
            order_id = data['orderID']
            orderSumm = data['orderSumm']
            status = "confirm"
            await confirmOrderStatus(order_id=int(order_id), summ=float(orderSumm), status=status)
            await message.answer(f"Заказ {order_id} успешно подтвержден")
            await message.answer(text=f"Главная (админка)", reply_markup=main_admin_kb())
            await state.clear()
        except ValueError:
            data = await state.get_data()
            order_id = data['orderID']
            await message.answer(f"Введите сумму для заказа {order_id}")








def register_add_order_admin_handlers(dp: Dispatcher):
    dp.callback_query.register(confirmOrder, F.data == "confirmOrder")
    dp.message.register(confirmOrderSumm, ConfirmOrderByIDState.getOrderID)
    dp.message.register(confirmOrderByID,ConfirmOrderByIDState.confirmOrder)
    dp.message.register(setOrderSumm, ConfirmOrderByIDState.setSumm)
