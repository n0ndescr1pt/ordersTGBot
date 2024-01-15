from aiogram.filters.callback_data import CallbackData

class NumbersCallbackFactoryEdit(CallbackData, prefix="galery_edit"):
    id: int

class NumbersCallbackFactoryDelete(CallbackData, prefix="galery_delete"):
    id: int


class NumbersCallbackFactoryConfirmOrder(CallbackData, prefix="confirm_order"):
    id: int

class NumbersCallbackFactorySetOrderUsPaid(CallbackData, prefix="paid_order"):
    id: int

class NumbersCallbackFactoryDeleteOrder(CallbackData, prefix="delete_order"):
    id: int