from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


def main_admin_kb():
    builder = InlineKeyboardBuilder()

    builder.button(text="Настройки", callback_data="Настройки"),
    builder.button(text="Добавить заказ", callback_data="Добавить заказ")

    builder.button(text="Выгрузить статистику", callback_data="uploadStat"),
    builder.button(text="Сообщение пользователю", callback_data="Сообщение пользователю")

    builder.adjust(2)

    return builder.as_markup(resize_keyboard=True)


def settings_kb():
    builder = InlineKeyboardBuilder()

    builder.button(text="Загрузить ФИД", callback_data="Загрузить ФИД"),
    builder.button(text="Обновить прайс лист", callback_data="обновитьПрайсЛист")

    builder.button(text="Редактировать галереи", callback_data="Редактировать галереи"),
    builder.button(text="Скачать ФИД", callback_data="Скачать ФИД")

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