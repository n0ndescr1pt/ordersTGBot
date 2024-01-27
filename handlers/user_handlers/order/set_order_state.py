from aiogram import Dispatcher, types
from aiogram.fsm.context import FSMContext

from data.database.function import deleteOrderFromDB, confirmOrderPaid, getOrderStatus, confirmOrderStatus
from keyboards.admin_kb import setOrderAsReadyToSend_kb, setOrderAsPaid_kb, confirm_order_kb
from utils.callbackFactory import NumbersCallbackFactoryConfirmOrder, NumbersCallbackFactoryDeleteOrder, \
    NumbersCallbackFactorySetOrderAsReadyToSend, NumbersCallbackFactorySetOrderUsPaid, \
    NumbersCallbackFactoryCancelOrder, NumbersCallbackFactoryCalcOrder
from utils.someMethods import cancelConfirmOrder, cancelCalcOrder
from utils.states import ConfirmOrderState



async def calcOrder(callback: types.CallbackQuery, callback_data: NumbersCallbackFactoryCalcOrder):
    user_id = await confirmOrderPaid(callback_data.id, "calculated")
    await callback.message.edit_text(text=callback.message.text,reply_markup=await confirm_order_kb(callback_data.id))
    await callback.message.answer(f"Заказ {callback_data.id} рассчитан")
    await callback.bot.send_message(chat_id=user_id[0], text=f"Заказ под номером {callback_data.id} был рассчитан")

async def confirmOrder(callback: types.CallbackQuery, state: FSMContext, callback_data: NumbersCallbackFactoryConfirmOrder):
    if (callback.message.text == "Отмена"):
        await cancelCalcOrder(callback.message, state)
    else:
        await state.update_data(orderID=callback_data.id)
        await callback.message.edit_text(text=callback.message.text,reply_markup=await setOrderAsPaid_kb(callback_data.id))
        await callback.message.answer(f"Введите сумму за этот заказ")
        await state.set_state(ConfirmOrderState.setSumm)

async def confirmOrderSumm(message: types.Message, state: FSMContext):
    if (message.text == "Отмена"):
        await cancelConfirmOrder(message, state)
    else:
        data = await state.get_data()
        order_id = data['orderID']
        order_status = await getOrderStatus(order_id)
        if(order_status[0]=="confirm"):
            await message.answer(f"Заказ {order_id} уже подтвежден")
        elif (order_status[0] == "paid"):
            await message.answer(f"Заказ {order_id} уже оплачен")
        else:
            try:
                await state.update_data(orderSumm=message.text)
                data = await state.get_data()
                order_id = data['orderID']
                orderSumm = data['orderSumm']
                status = "confirm"
                await confirmOrderStatus(order_id=int(order_id),summ=float(orderSumm), status=status)
                await message.answer(f"Заказ {order_id} успешно подтвержден")
                await message.bot.send_message(chat_id=order_status[2],text=f"По заказу номер {order_id} вам выставлен счет на оплату")
                await state.clear()
            except ValueError:
                data = await state.get_data()
                order_id = data['orderID']
                await message.answer(f"Введите сумму для заказа {order_id}")



async def SetOrderUsPaid(callback: types.CallbackQuery, callback_data: NumbersCallbackFactorySetOrderUsPaid):
    order_status = await getOrderStatus(callback_data.id)
    if (order_status[0] == "paid"):
        await callback.message.answer(f"Заказ {callback_data.id} уже подтвежден")
    else:
        user_id = await confirmOrderPaid(callback_data.id, "paid")
        await callback.message.edit_text(text=callback.message.text,reply_markup=await setOrderAsReadyToSend_kb(callback_data.id))
        await callback.message.answer(f"Заказ {callback_data.id} отмечен как оплачен")
        await callback.bot.send_message(chat_id=user_id[0],text=f"Оплата заказа на сумму {order_status[1]} подтверждена, заказ находится в обработке")

async def SetOrderAsReadyToSend(callback: types.CallbackQuery, callback_data: NumbersCallbackFactorySetOrderAsReadyToSend):
    user_id = await confirmOrderPaid(callback_data.id, "readyToSend")
    await callback.message.answer(f"Заказ {callback_data.id} отмечен как готов к отправке")
    await callback.bot.send_message(chat_id=user_id[0],text=f"Заказ под номером {callback_data.id} готов к отправке")
    await callback.message.delete()


async def deleteOrder(callback: types.CallbackQuery, callback_data: NumbersCallbackFactoryDeleteOrder):
    await deleteOrderFromDB(callback_data.id)
    await callback.message.answer(f"Заказ {callback_data.id} удален")
    await callback.message.delete()

async def cancelOrder(callback: types.CallbackQuery, callback_data: NumbersCallbackFactoryCancelOrder):
    user_id = await confirmOrderPaid(callback_data.id, "canceled")
    await callback.message.answer(f"Заказ {callback_data.id} отменен")
    await callback.bot.send_message(chat_id=user_id[0], text=f"Заказ под номером {callback_data.id} отменен")



def register_services_set_orderState_user_handlers(dp: Dispatcher):
    dp.callback_query.register(confirmOrder, NumbersCallbackFactoryConfirmOrder.filter())
    dp.callback_query.register(deleteOrder, NumbersCallbackFactoryDeleteOrder.filter())
    dp.message.register(confirmOrderSumm, ConfirmOrderState.setSumm)
    dp.callback_query.register(SetOrderAsReadyToSend, NumbersCallbackFactorySetOrderAsReadyToSend.filter())

    dp.callback_query.register(SetOrderUsPaid, NumbersCallbackFactorySetOrderUsPaid.filter())
    dp.callback_query.register(cancelOrder, NumbersCallbackFactoryCancelOrder.filter())
    dp.callback_query.register(calcOrder, NumbersCallbackFactoryCalcOrder.filter())