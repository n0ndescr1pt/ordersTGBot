from aiogram.fsm.state import StatesGroup, State


class CheckAdminState(StatesGroup):
    password = State()


#состояния для калькуляции стоимости
class PreOrderState(StatesGroup):
    countPack = State()
    volume = State()
    needPurchase = State()
    type = State()


#состояния для отправки прайс листа админом
class UpdatePriceListState(StatesGroup):
    updatePriceList = State()

class OrderState(StatesGroup):
    countPack = State()
    volume = State()
    needPurchase = State()
    type = State()
