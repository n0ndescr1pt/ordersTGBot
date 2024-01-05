from aiogram import types, Dispatcher, F

from keyboards.admin_kb import settings_kb


async def setting(callback: types.CallbackQuery):
    await callback.message.edit_text(f"Настройки", reply_markup=settings_kb())









def register_settings_admin_handlers(dp: Dispatcher):
    dp.callback_query.register(setting, F.data == "Настройки")
