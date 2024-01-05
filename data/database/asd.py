import sqlite3

connection = sqlite3.connect('database.db')
connection.execute("create table users (user_id INTEGER PRIMARY KEY AUTOINCREMENT, id int not null, name varchar(50))")
connection.execute("create table orders (order_id INTEGER PRIMARY KEY AUTOINCREMENT, , name varchar(50))")
connection.commit()
connection.close()