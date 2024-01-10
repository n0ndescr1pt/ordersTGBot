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


#состояния для создания заказа
class OrderState(StatesGroup):
    getPhone = State()
    setBonus = State()
    countBonus = State()
    addFile = State()



#galery


class Galery(StatesGroup):
    choose = State()
    getGaleryPhoto = State()
    getGaleryCaption = State()

class EditMarketplace(StatesGroup):
    getPhoto = State()
    setCaption = State()



