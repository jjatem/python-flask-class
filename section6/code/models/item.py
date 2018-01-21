import sqlite3

class ItemModel:
    TABLE_NAME = 'items'
    
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def json(self):
        return { 'name' : self.name, 'price': self.price }

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM {table} WHERE name=?".format(table=cls.TABLE_NAME)
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()

        if row:
            return {'item': {'name': row[0], 'price': row[1]}}

    @classmethod
    def insert(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        insert_query = "INSERT INTO {table_name} VALUES (?,?)".format(table_name=cls.TABLE_NAME)
        cursor.execute(insert_query, (item['name'], item['price']))
        connection.commit()

        cursor.close()
        connection.close()

    @classmethod
    def update(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        update_query = "UPDATE {table_name} SET price = ? WHERE name = ?".format(table_name=cls.TABLE_NAME)
        cursor.execute(update_query, (item['price'], item['name']))
        connection.commit()

        cursor.close()
        connection.close()
