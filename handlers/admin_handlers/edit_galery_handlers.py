import json

from aiogram import types, Dispatcher, F
from aiogram.fsm.context import FSMContext


from data.database.function import addGalery, deleteGalery
from keyboards.admin_kb import edit_galery_kb, edit_kb, add_photo_kb, \
    edit_galery_items_kb, delete_galery_items_kb
from utils.callbackFactory import NumbersCallbackFactoryEdit, NumbersCallbackFactoryDelete
from utils.someMethods import cancelEditGalery, getGaleryItems
from utils.states import Galery


async def main_edit_galery(callback: types.CallbackQuery):
    await callback.message.edit_text(f"Редактировать галареи", reply_markup=edit_galery_kb())


async def edit_marketplace(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer(f"редактирование маркетплейса", reply_markup=edit_kb())
    await state.update_data(galery_id="marketplace")
    await state.set_state(Galery.choose)


async def edit_fullfillment(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer(f"редактирование фуллфиллмента", reply_markup=edit_kb())
    await state.update_data(galery_id="fullfillment")
    await state.set_state(Galery.choose)

async def edit_present(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer(f"редактирование подарков", reply_markup=edit_kb())
    await state.update_data(galery_id="present")
    await state.set_state(Galery.choose)

async def edit_individual_pack(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer(f"редактирование индивидуальной упаковки", reply_markup=edit_kb())
    await state.update_data(galery_id="individualPack")
    await state.set_state(Galery.choose)

async def choose_edit_delete_galery(message: types.Message, state: FSMContext):
    imgs = []
    await state.update_data(imgs=imgs)
    if (message.text == "Отмена"):
        await cancelEditGalery(message, state)
    else:
        if(message.text == "Добавить"):
            await message.answer(f"Отправьте до 10 фотографий",reply_markup=add_photo_kb())
            await state.set_state(Galery.getGaleryPhoto)

        elif(message.text == "Изменить"):
            data = await state.get_data()
            await getGaleryItems(message, data['galery_id'],data['galery_id'])

            await message.answer(f"Выберите элемент который нужно изменить",reply_markup=await edit_galery_items_kb(data['galery_id']))

        elif (message.text == "Удалить"):
            data = await state.get_data()
            await getGaleryItems(message, data['galery_id'],data['galery_id'])

            await message.answer(f"Выберите элемент который нужно изменить",reply_markup=await delete_galery_items_kb(data['galery_id']))



async def edit_galery(callback: types.CallbackQuery, state: FSMContext, callback_data: NumbersCallbackFactoryEdit):
    if (callback.message.text == "Отмена"):
        await cancelEditGalery(callback.message, state)
    await deleteGalery(callback_data.id)
    await callback.message.answer(f"Отправьте до 10 фотографий", reply_markup=add_photo_kb())
    await state.set_state(Galery.getGaleryPhoto)


async def delete_galery(callback: types.CallbackQuery, state: FSMContext, callback_data: NumbersCallbackFactoryEdit):
    if (callback.message.text == "Отмена"):
        await cancelEditGalery(callback.message, state)
    await deleteGalery(callback_data.id)
    await callback.message.answer(f"Успешно удалено")
    await callback.message.answer(f"Редактировать галареи", reply_markup=edit_galery_kb())






#добавление
async def get_galery_photo(message: types.Message, state: FSMContext):
    data = await state.get_data()
    if (message.text == "Отмена"):
        await cancelEditGalery(message, state)
    elif(message.text == "Готово"):
        await state.update_data(photos=json.dumps(data['imgs']))
        await message.answer(f"Отправьте описание",reply_markup=add_photo_kb())
        await state.set_state(Galery.getGaleryCaption)
    else:
        photos = message.photo
        data['imgs'].append(photos[0].file_id)

async def get_galery_caption(message: types.Message, state: FSMContext):
    if (message.text == "Отмена"):
        await cancelEditGalery(message, state)
    else:
        await state.update_data(caption=message.text)
        data = await state.get_data()
        await addGalery(data["galery_id"],data["photos"],data["caption"])
        await message.answer(f"Успешно добавлено")
        await message.answer(f"Редактировать галареи", reply_markup=edit_galery_kb())
        await state.clear()


#документы
#сумма
#сумма без скидки
#сообщение пользователю

#поддтверждение второй раз что оплачено
def register_edit_galery_admin_handlers(dp: Dispatcher):
    dp.callback_query.register(main_edit_galery, F.data == "Редактировать галереи")

    dp.callback_query.register(edit_marketplace, F.data == "edit_Маркетплейсы")
    dp.callback_query.register(edit_present, F.data == "edit_Подарки")
    dp.callback_query.register(edit_individual_pack, F.data == "edit_Индивидуальная упаковка")
    dp.callback_query.register(edit_fullfillment, F.data == "edit_Фулфилмент")

    dp.message.register(choose_edit_delete_galery, Galery.choose)
    dp.message.register(get_galery_photo, Galery.getGaleryPhoto)
    dp.message.register(get_galery_caption, Galery.getGaleryCaption)

    dp.callback_query.register(edit_galery, NumbersCallbackFactoryEdit.filter())
    dp.callback_query.register(delete_galery, NumbersCallbackFactoryDelete.filter())