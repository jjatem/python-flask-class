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

        query = "SELECT * FROM {table} WHERE name=?".format(table=ItemModel.TABLE_NAME)
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()

        if row:
            return cls(*row)

    def insert(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        insert_query = "INSERT INTO {table_name} VALUES (?,?)".format(table_name=ItemModel.TABLE_NAME)
        cursor.execute(insert_query, (self.name, self.price))
        connection.commit()

        cursor.close()
        connection.close()

    def update(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        update_query = "UPDATE {table_name} SET price = ? WHERE name = ?".format(table_name=ItemModel.TABLE_NAME)
        cursor.execute(update_query, (self.price, self.name))
        connection.commit()

        cursor.close()
        connection.close()
