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

users = [
    (3,'Sandy','test01'),
    (4,'John','test01'),
    (5,'Kate','test01')
]

cursor.executemany(insert_query, users)

connection.commit()

select_query = "SELECT * FROM users;"

for row in cursor.execute(select_query):
    print("UserId: {}. Username: {}. Password: {}".format(row[0],row[1],row[2]))

for row in cursor.execute(select_query):
    print(row)

cursor.close()
connection.close()
