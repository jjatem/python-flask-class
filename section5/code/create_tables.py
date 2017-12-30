import sqlite3

users = [
    (1,'Joe','asdf'),
    (2,'joffre', 'test01'),
    (3,'Sandy','test01'),
    (4,'John','test01'),
    (5,'Kate','test01')
]

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

drop_table = "DROP TABLE IF EXISTS users;"
create_table = "CREATE TABLE users (id int PRIMARY KEY,username text UNIQUE, password text);"
insert_query = "INSERT INTO users values (?, ?, ?)"

cursor.execute(drop_table)
cursor.execute(create_table)
cursor.executemany(insert_query, users)

connection.commit()

select_query = "SELECT * FROM users;"

for row in cursor.execute(select_query):
    print(row)
