from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


def main_kb():
    builder = InlineKeyboardBuilder()

    builder.button(text="Галерея", callback_data="Галерея"),
    builder.button(text="О нас", callback_data="О нас")

    builder.button(text="Бонусная программа", callback_data="Бонусная программа"),
    builder.button(text="Услуги", callback_data="Услуги")

    builder.adjust(2)

    return builder.as_markup(resize_keyboard=True)


def bonus_kb():
    builder = InlineKeyboardBuilder()

    builder.button(text="Баланс", callback_data="Баланс"),
    builder.button(text="Условия", callback_data="Условия")

    builder.button(text="Учавствовать", callback_data="Учавствовать"),
    builder.button(text="Услуги", callback_data="Услуги")

    builder.button(text="Назад", callback_data="Назад")

    builder.adjust(2)

    return builder.as_markup(resize_keyboard=True)

def galery_kb():
    builder = InlineKeyboardBuilder()

    builder.button(text="Маркетплейсы", callback_data="Маркетплейсы"),
    builder.button(text="Подарки", callback_data="Подарки")

    builder.button(text="Индивидуальная упаковка", callback_data="Индивидуальная упаковка"),
    builder.button(text="Фулфилмент", callback_data="Фулфилмент")

    builder.button(text="Назад", callback_data="Назад")

    builder.adjust(2)

    return builder.as_markup(resize_keyboard=True)


def aboutUs_kb():
    builder = InlineKeyboardBuilder()

    builder.button(text="О компании",callback_data="О компании"),
    builder.button(text="Галерея", callback_data="Галерея")

    builder.button(text="Услуги", callback_data="Услуги"),
    builder.button(text="Юридическая информация", callback_data="Юридическая информация")

    builder.button(text="Назад", callback_data="Назад")

    builder.adjust(2)

    return builder.as_markup(resize_keyboard=True)

def services_kb():
    builder = InlineKeyboardBuilder()

    builder.button(text="Прайс лист", callback_data="Прайс лист"),
    builder.button(text="Связь со спецом", callback_data="Связь со спецом")

    builder.button(text="Оформить заказ", callback_data="Оформить заказ"),
    builder.button(text="Предварительный расчет", callback_data="Предварительный расчет")

    builder.button(text="Назад", callback_data="Назад")

    builder.adjust(2)

    return builder.as_markup(resize_keyboard=True)

#---------main button

