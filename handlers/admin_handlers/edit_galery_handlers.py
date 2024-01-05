from aiogram import types, Dispatcher, F

from keyboards.admin_kb import edit_galery_kb


async def edit_galery(callback: types.CallbackQuery):
    await callback.message.edit_text(f"Редактировать галареи", reply_markup=edit_galery_kb())









def register_edit_galery_admin_handlers(dp: Dispatcher):
    dp.callback_query.register(edit_galery, F.data == "Редактировать галереи")
