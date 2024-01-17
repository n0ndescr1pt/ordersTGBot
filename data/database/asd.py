import sqlite3

connection = sqlite3.connect('database.db')
#connection.execute("create table users (user_id int PRIMARY KEY, name varchar(50), balance float)")
connection.execute("update users set balance = 10")
#connection.execute("create table orders (order_id INTEGER PRIMARY KEY AUTOINCREMENT, user_id int, bonus_decrease int, name varchar(32) , phone varchar(32), files text, count_packs varchar(32), volume varchar(32), needPurchase varchar(32),ratio varchar(32), calc_summ float, status varchar(32), real_summ float, summ_with_bonus float, FOREIGN KEY(user_id) REFERENCES users(user_id))")
#connection.execute("create table galery (id INTEGER PRIMARY KEY AUTOINCREMENT, galery_id varchar(32), images text, caption text)")
connection.commit()
connection.close()