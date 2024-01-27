from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from data.database.function import selectGalery, selectOrder
from utils.callbackFactory import NumbersCallbackFactoryEdit, NumbersCallbackFactoryDelete, \
    NumbersCallbackFactoryConfirmOrder, NumbersCallbackFactorySetOrderUsPaid, NumbersCallbackFactoryDeleteOrder, \
    NumbersCallbackFactorySetOrderAsReadyToSend, NumbersCallbackFactoryCalcOrder, NumbersCallbackFactoryCancelOrder


def main_admin_kb():
    builder = InlineKeyboardBuilder()

    builder.button(text="Настройки", callback_data="Настройки"),
    builder.button(text="Добавить заказ", callback_data="confirmOrder")

    builder.button(text="Выгрузить статистику", callback_data="uploadStat"),
    builder.button(text="Сообщение пользователю", callback_data="sendMessageToUser")

    builder.adjust(2)

    return builder.as_markup(resize_keyboard=True)


def settings_kb():
    builder = InlineKeyboardBuilder()

    builder.button(text="Загрузить ФИД", callback_data="uploadFeed"),
    builder.button(text="Обновить прайс лист", callback_data="обновитьПрайсЛист")

    builder.button(text="Редактировать галереи", callback_data="Редактировать галереи"),
    builder.button(text="Скачать ФИД", callback_data="downloadFeed")

    builder.button(text="Назад", callback_data="Назад_admin")

    builder.adjust(2)

    return builder.as_markup(resize_keyboard=True)

def cancel_kb():
    kb = [
        [
            types.KeyboardButton(text="Отмена"),
        ],
    ]
    backKeyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        one_time_keyboard=True,
        resize_keyboard=True,
    )
    return backKeyboard

def edit_galery_kb():
    builder = InlineKeyboardBuilder()

    builder.button(text="Маркетплейсы", callback_data="edit_Маркетплейсы"),
    builder.button(text="Подарки", callback_data="edit_Подарки")

    builder.button(text="Индивидуальная упаковка", callback_data="edit_Индивидуальная упаковка"),
    builder.button(text="Фулфилмент", callback_data="edit_Фулфилмент")

    builder.button(text="Назад", callback_data="Назад_admin")

    builder.adjust(2)

    return builder.as_markup(resize_keyboard=True)


def edit_kb():
    kb = [
        [
            types.KeyboardButton(text="Добавить"),
            types.KeyboardButton(text="Изменить"),
            types.KeyboardButton(text="Удалить")
        ],
        [types.KeyboardButton(text="Отмена"),],

    ]
    backKeyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        one_time_keyboard=True,
        resize_keyboard=True,
    )
    return backKeyboard

def add_photo_kb():
    kb = [
        [
            types.KeyboardButton(text="Готово"),
        ],
        [
            types.KeyboardButton(text="Отмена")
        ],

    ]
    backKeyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        one_time_keyboard=True,
        resize_keyboard=True,
    )
    return backKeyboard


async def edit_galery_items_kb(galeryID):
    builder = InlineKeyboardBuilder()
    i=0
    galeryItems = await selectGalery(galeryID)
    for item in galeryItems:
        i+=1
        builder.button(text=f"{i}", callback_data=NumbersCallbackFactoryEdit(id=item[0])),

    builder.adjust(1)

    return builder.as_markup()

async def delete_galery_items_kb(galeryID):
    builder = InlineKeyboardBuilder()
    i=0
    galeryItems = await selectGalery(galeryID)
    for item in galeryItems:
        i+=1
        builder.button(text=f"{i}", callback_data=NumbersCallbackFactoryDelete(id=item[0])),

    builder.adjust(1)

    return builder.as_markup()


async def calculate_order_kb(orderdID):
    builder = InlineKeyboardBuilder()
    builder.button(text=f"Отметить заказ как рассчитан", callback_data=NumbersCallbackFactoryCalcOrder(id=orderdID)),
    builder.button(text=f"Отменить", callback_data=NumbersCallbackFactoryCancelOrder(id=orderdID)),
    builder.button(text=f"Удалить", callback_data=NumbersCallbackFactoryDeleteOrder(id=orderdID))

    builder.adjust(1)

    return builder.as_markup()

async def confirm_order_kb(orderdID):
    builder = InlineKeyboardBuilder()
    builder.button(text=f"Подтвердить", callback_data=NumbersCallbackFactoryConfirmOrder(id=orderdID)),
    builder.button(text=f"Отменить", callback_data=NumbersCallbackFactoryCancelOrder(id=orderdID)),
    builder.button(text=f"Удалить", callback_data=NumbersCallbackFactoryDeleteOrder(id=orderdID))
    builder.adjust(1)

    return builder.as_markup()

async def setOrderAsPaid_kb(orderdID):
    builder = InlineKeyboardBuilder()
    builder.button(text=f"Отметить как оплаченный", callback_data=NumbersCallbackFactorySetOrderUsPaid(id=orderdID)),
    builder.button(text=f"Отменить", callback_data=NumbersCallbackFactoryCancelOrder(id=orderdID)),
    builder.button(text=f"Удалить", callback_data=NumbersCallbackFactoryDeleteOrder(id=orderdID))
    builder.adjust(1)

    return builder.as_markup()

async def setOrderAsReadyToSend_kb(orderdID):
    builder = InlineKeyboardBuilder()
    builder.button(text=f"Отметить как готов к отгрузке", callback_data=NumbersCallbackFactorySetOrderAsReadyToSend(id=orderdID)),
    builder.button(text=f"Отменить", callback_data=NumbersCallbackFactoryCancelOrder(id=orderdID)),
    builder.button(text=f"Удалить", callback_data=NumbersCallbackFactoryDeleteOrder(id=orderdID))
    builder.adjust(1)

    return builder.as_markup()


