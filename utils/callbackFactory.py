from aiogram.filters.callback_data import CallbackData

class NumbersCallbackFactoryEdit(CallbackData, prefix="galery_edit"):
    id: int

class NumbersCallbackFactoryDelete(CallbackData, prefix="galery_delete"):
    id: int