from flask_restful import Resource, reqparse
from flask_jwt import jwt_required, current_identity
import sqlite3

items = []

class Item(Resource):
    TABLE_NAME = 'items'

    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field cannot be left blank and it has to be a valid Float number!"
    )

    @jwt_required()
    def get(self, name):
        item = self.find_by_name(name)
        if item:
            return item
        return {'message': 'Item not found'}, 404

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

    def post(self, name):
        if self.find_by_name(name):
            return {'message': "An item with name [{}] already exists".format(name)}, 409

        data = Item.parser.parse_args()
        item = {'name': name, 'price' : data['price']}

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        insert_query = "INSERT INTO {table_name} VALUES (?,?)".format(table_name=Item.TABLE_NAME)
        cursor.execute(insert_query, (item['name'], item['price']))
        connection.commit()

        cursor.close()
        connection.close()
        return item, 201

    @jwt_required()
    def delete(self, name):

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        delete_query = "DELETE FROM {table_name} WHERE name = ?".format(table_name=Item.TABLE_NAME)

        cursor.execute(delete_query, (name,))
        connection.commit()

        cursor.close()
        connection.close()        
        return {'message': 'Item deleted'}

    #@jwt_required()
    def put(self, name):
        data = Item.parser.parse_args()
        item = next(filter(lambda x: x['name'] == name, items), None)
        if item is None:
            item = {'name': name, 'price' : data['price']}
            items.append(item)
        else:
            item.update(data)
        return item


class ItemList(Resource):
    TABLE_NAME = 'items'

    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM {table}".format(table=self.TABLE_NAME)
        result = cursor.execute(query)

        items = []
        for row in result:
            items.append({'name': row[0], 'price': row[1]})

        connection.close()

        return {'items': items}
