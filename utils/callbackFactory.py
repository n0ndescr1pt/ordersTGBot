from aiogram.filters.callback_data import CallbackData

class NumbersCallbackFactoryEdit(CallbackData, prefix="galery_edit"):
    id: int

class NumbersCallbackFactoryDelete(CallbackData, prefix="galery_delete"):
    id: int


class NumbersCallbackFactoryCalcOrder(CallbackData, prefix="calc_order"):
    id: int
class NumbersCallbackFactoryConfirmOrder(CallbackData, prefix="cencel_order"):
    id: int


class NumbersCallbackFactorySetOrderUsPaid(CallbackData, prefix="paid_order"):
    id: int


class NumbersCallbackFactorySetOrderAsReadyToSend(CallbackData, prefix="ready_to_send_order"):
    id: int

class NumbersCallbackFactoryDeleteOrder(CallbackData, prefix="delete_order"):
    id: int

class NumbersCallbackFactoryCancelOrder(CallbackData, prefix="cancel_order"):
    id: int

class CoefficientPreOrder(CallbackData, prefix="coefficient"):
    coefficient: float