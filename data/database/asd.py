import sqlite3

connection = sqlite3.connect('database.db')
connection.execute("update users set balance = 500 where user_id = 713246526")
#connection.execute("create table users (user_id int PRIMARY KEY, name varchar(50), balance float, phone varchar(32), first_name varchar(32))")
#connection.execute("delete from orders where order_id > 0")
#connection.execute("create table orders (order_id INTEGER PRIMARY KEY AUTOINCREMENT, user_id int, bonus_decrease int, name varchar(32) , phone varchar(32), files text, count_packs varchar(32), volume varchar(32), needPurchase varchar(32),ratio varchar(32), calc_summ float, status varchar(32), real_summ float, summ_with_bonus float, FOREIGN KEY(user_id) REFERENCES users(user_id))")
#connection.execute("create table galery (id INTEGER PRIMARY KEY AUTOINCREMENT, galery_id varchar(32), images text, caption text)")
connection.commit()
connection.close()