import sqlite3

connection = sqlite3.connect('data.db')

cursor = connection.cursor()

drop_table = "DROP TABLE IF EXISTS users;"

create_table = "CREATE TABLE users (id int PRIMARY KEY,username text UNIQUE, password text);"

cursor.execute(drop_table)
cursor.execute(create_table)

user = (1,'Joe','asdf')
second_user = (2,'joffre', 'test01')

insert_query = "INSERT INTO users values (?, ?, ?)"

cursor.execute(insert_query, user)
cursor.execute(insert_query, second_user)

connection.commit()

cursor.close()
connection.close()
