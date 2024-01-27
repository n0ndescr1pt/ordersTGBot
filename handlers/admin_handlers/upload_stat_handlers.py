import json

from aiogram import types, Dispatcher, F
from aiogram.types import FSInputFile

from data.database.function import getStats, getUsers
from keyboards.admin_kb import main_admin_kb


async def uploadStat(callback: types.CallbackQuery):
    await callback.message.delete()
    stat = await getStats()
    users = await getUsers()
    n_data = {}
    for user in users:
        n_data[user[1]] = {"orders":{}}
        i = 0
        for order in stat:
            if(order[0] == user[0]):
                if (order[17] == None):
                    bonus = 0
                else:
                    bonus = int(order[17]) * 0.05
                i+=1
                n_data[user[1]]["orders"][i] = {"name":order[4],
                                                "phone":order[3],
                                                "email": order[19],
                                                "bonus_decreased": order[7],
                                                "bonus_added": bonus,
                                                "summ": order[17],
                                                "summ_with_bonus": order[18],
                                                "status": order[16],
                                                "order_id": order[2]
                                                }


        n_data[user[1]]["balance"] = user[2]
    with open("data/stats.json", "w", encoding='utf-8') as outf:
        json.dump(n_data, outf, ensure_ascii=False, indent=4)

    statistics = FSInputFile("data/stats.json")
    await callback.message.answer_document(document=statistics,caption=f"Статистика по всем пользовтаелям успешно выгружена")
    await callback.message.answer(f"Главная (админка)", reply_markup=main_admin_kb())







def register_upload_stat_admin_handlers(dp: Dispatcher):
    dp.callback_query.register(uploadStat, F.data == "uploadStat")
