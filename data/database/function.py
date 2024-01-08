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
