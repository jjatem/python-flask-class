from flask_restful import Resource, reqparse
from flask_jwt import jwt_required, current_identity
from models.item import ItemModel
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
        item = ItemModel.find_by_name(name)
        if item:
            return item
        return {'message': 'Item not found'}, 404


    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': "An item with name [{}] already exists".format(name)}, 409

        data = Item.parser.parse_args()
        item = {'name': name, 'price' : data['price']}

        try:
            ItemModel.insert(item)
        except:
            return {"message": "An error occurred inserting the item."}, 500 #internal server error

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
        item = ItemModel.find_by_name(name)
        updated_item = {'name': name, 'price': data['price']}
        if item is None:
            try:
                ItemModel.insert(updated_item)
            except:
                return {"message": "An error occurred inserting the item."}, 500
        else:
            try:
                ItemModel.update(updated_item)
            except:
                raise
                return {"message": "An error occurred updating the item."}, 500

        return updated_item


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
