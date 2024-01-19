from aiogram.fsm.state import StatesGroup, State


class CheckAdminState(StatesGroup):
    password = State()
    wrongPassword = State()


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
    setPhone = State()
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


class ConfirmOrderState(StatesGroup):
    setSumm = State()

class ConfirmOrderByIDState(StatesGroup):
    getOrderID = State()
    confirmOrder = State()
    setSumm = State()

class UpdateFeedState(StatesGroup):
    updateFeed = State()

class SendMessageToUserState(StatesGroup):
    getUsername = State()
    getMessage = State()