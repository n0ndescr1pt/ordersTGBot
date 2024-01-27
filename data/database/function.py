import sqlite3

#добавить нового пользователя в бд
def addUser(user_id: int, name):
    connection = sqlite3.connect('data/database/database.db')
    cursor = connection.cursor()
    info = cursor.execute("SELECT user_id FROM users WHERE user_id = (?)", (user_id,)).fetchone()
    if(info == None):
        connection.execute("INSERT INTO users (user_id,name,balance) VALUES (?, ?, ?)", (user_id,f"@{name}",0))
    connection.commit()
    connection.close()

#посмотреть баланс пользователя
async def getBalance(user_id: int):
    connection = sqlite3.connect('data/database/database.db')
    cursor = connection.cursor()
    balance = cursor.execute("SELECT balance FROM users WHERE user_id = (?)",(user_id,)).fetchone()
    connection.close()
    return balance


async def insertOrder(user_id: int, bonus_balance, name, phone, docs_id,status,email):
    connection = sqlite3.connect('data/database/database.db')
    orderID = connection.execute("INSERT INTO orders (user_id, bonus_decrease, name, phone, files, status,email) VALUES (?,?,?,?,?,?,?)", (user_id, bonus_balance, name, phone, docs_id, status, email)).lastrowid
    connection.commit()
    connection.close()
    return orderID

async def insertOrderWithCalc(user_id: int, bonus_balance, name, phone, docs_id, count_packs, volume,needPurchase, ratio, calc_summ, status, email):
    connection = sqlite3.connect('data/database/database.db')
    orderID = connection.execute("INSERT INTO orders (user_id, bonus_decrease, name, phone, files, count_packs, volume,needPurchase, ratio, calc_summ, status, email) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",(user_id, bonus_balance, name, phone, docs_id,count_packs, volume,needPurchase, ratio, calc_summ, status,email)).lastrowid
    connection.commit()
    connection.close()
    return orderID


#вся статистика польщователей
async def getStats():
    connection = sqlite3.connect('data/database/database.db')
    cursor = connection.cursor()
    stat = cursor.execute("SELECT * FROM users INNER JOIN orders on orders.user_id = users.user_id").fetchall()
    connection.close()
    return stat

async def getUsers():
    connection = sqlite3.connect('data/database/database.db')
    cursor = connection.cursor()
    users = cursor.execute("SELECT user_id, name, balance FROM users ").fetchall()
    connection.close()
    return users

async def addGalery(galery_id, images, caption):
    connection = sqlite3.connect('data/database/database.db')
    connection.execute("INSERT INTO galery (galery_id, images, caption) VALUES (?,?,?)",   (galery_id, images, caption))
    connection.commit()
    connection.close()


#выборка обьектов галереи для создания клавиатуры
async def selectGalery(galery_id):
    connection = sqlite3.connect('data/database/database.db')
    cursor = connection.cursor()
    stat = cursor.execute("SELECT * FROM galery where galery_id = ?",(galery_id,)).fetchall()
    connection.close()
    return stat

#удаление нужного объекта
async def deleteGalery(galery_id: int):
    connection = sqlite3.connect('data/database/database.db')
    cursor = connection.cursor()
    cursor.execute("DELETE FROM galery WHERE id = (?)",(galery_id,))
    connection.commit()
    connection.close()


#достаем нужный заказ для последующего подтверждения его админом
async def selectOrder(order_id: int):
    connection = sqlite3.connect('data/database/database.db')
    cursor = connection.cursor()
    stat = cursor.execute("SELECT order_id FROM orders where order_id = ?", (order_id,)).fetchall()
    connection.close()
    return stat

async def confirmOrderStatus(order_id: int, summ: float, status):
    connection = sqlite3.connect('data/database/database.db')
    connection.execute(f"UPDATE orders set status = (?) WHERE order_id = (?) ",(status, order_id))
    connection.execute(f"UPDATE orders set real_summ = (?) WHERE order_id = (?) ", (summ, order_id))

    cursor = connection.cursor()
    summ_with_bonus = cursor.execute("SELECT bonus_decrease, real_summ, user_id FROM orders WHERE order_id = (?)", (order_id,)).fetchone()
    if(summ_with_bonus[0]>summ_with_bonus[1]):
        connection.execute(f"UPDATE orders set summ_with_bonus = 0 where order_id = (?) ",(order_id,))
        connection.execute(f"UPDATE users set balance = {summ_with_bonus[0]-summ_with_bonus[1]}+(select balance from users where user_id = {summ_with_bonus[2]}) WHERE user_id = {summ_with_bonus[2]} ")
    else:
        connection.execute(f"UPDATE orders set summ_with_bonus = {summ_with_bonus[1] - summ_with_bonus[0]} where order_id = (?) ", (order_id,))
    connection.commit()
    connection.close()

async def confirmOrderPaid(order_id: int, status):
    connection = sqlite3.connect('data/database/database.db')
    connection.execute(f"UPDATE orders set status = (?) WHERE order_id = (?) ",(status, order_id))

    cursor = connection.cursor()
    user_id = cursor.execute("SELECT user_id FROM orders WHERE order_id = (?)",
                                     (order_id,)).fetchone()
    connection.execute(f"UPDATE users set balance = (select real_summ*0.05+(select balance from users where user_id = {user_id[0]}) from orders WHERE order_id = (?)) WHERE user_id = {user_id[0]} ", (order_id,))
    connection.execute(f"UPDATE users set balance = (select balance-(select bonus_decrease from orders where order_id = (?)) from users where user_id = {user_id[0]}) WHERE user_id = {user_id[0]} ",(order_id,))
    cursor = connection.cursor()
    user_id = cursor.execute("SELECT user_id FROM orders WHERE order_id = (?)", (order_id,)).fetchone()
    connection.commit()
    connection.close()
    return user_id

async def deleteOrderFromDB(order_id: int):
    connection = sqlite3.connect('data/database/database.db')
    connection.execute("DELETE FROM orders WHERE order_id=?", (order_id,))
    connection.commit()
    connection.close()

async def getOrderStatus(order_id: int):
    connection = sqlite3.connect('data/database/database.db')
    cursor = connection.cursor()
    stat = cursor.execute("SELECT status, real_summ, user_id FROM orders where order_id = ?", (order_id,)).fetchone()
    connection.close()
    return stat

async def getUserPhoneAndName(user_id: int):
    connection = sqlite3.connect('data/database/database.db')
    cursor = connection.cursor()
    stat = cursor.execute("SELECT phone,first_name FROM users where user_id = ?", (user_id,)).fetchone()
    connection.close()
    return stat
async def setUserPhoneAndName(user_id: int, phone, first_name):
    connection = sqlite3.connect('data/database/database.db')
    connection.execute("update users set phone = ? where user_id = ?", (phone,user_id))
    connection.execute("update users set first_name = ? where user_id = ?", (first_name, user_id))
    connection.commit()
    connection.close()

async def getUserIDfromNickname(nickname):
    connection = sqlite3.connect('data/database/database.db')
    cursor = connection.cursor()
    stat = cursor.execute("SELECT user_id FROM users where name = ?", (nickname,)).fetchone()
    connection.close()
    return stat

async def updateGalery(galery_id, images, caption):
    connection = sqlite3.connect('data/database/database.db')
    connection.execute("insert into galery (galery_id,images, caption) VALUES (?,?,?)", (galery_id,images,caption))
    connection.commit()
    connection.close()


async def deleteAllGalery():
    connection = sqlite3.connect('data/database/database.db')
    connection.execute("DELETE FROM galery WHERE id > 0")
    connection.commit()
    connection.close()
