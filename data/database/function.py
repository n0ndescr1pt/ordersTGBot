import sqlite3

#добавить нового пользователя в бд
def addUser(user_id: int, name):
    connection = sqlite3.connect('data/database/database.db')
    cursor = connection.cursor()
    info = cursor.execute("SELECT user_id FROM users WHERE user_id = (?)", (user_id,)).fetchone()
    if(info != None):
        connection.execute("DELETE FROM users WHERE user_id=?", (user_id,))
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


async def insertOrder(user_id: int, bonus_balance, name, phone, docs_id):
    connection = sqlite3.connect('data/database/database.db')
    connection.execute("INSERT INTO orders (user_id, bonus_balance, name, phone, files) VALUES (?,?,?,?,?)", (user_id, bonus_balance, name, phone, docs_id))
    connection.commit()
    connection.close()


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