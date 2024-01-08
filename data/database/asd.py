import sqlite3

connection = sqlite3.connect('database.db')
connection.execute("create table users (user_id int PRIMARY KEY, name varchar(50), balance float)")
#connection.execute("create table orders (order_id INTEGER PRIMARY KEY AUTOINCREMENT, , name varchar(50))")
connection.commit()
connection.close()