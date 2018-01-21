import sqlite3
from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from models.user import User

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
        type=str,
        required=True,
        help="Username must be provided."
    )
    parser.add_argument('password',
        type=str,
        required=True,
        help="Password must be provided."
    )

    def post(self):
        data = UserRegister.parser.parse_args()

        new_username = data['username']

        if User.find_by_username(new_username):
            return {'message': "Cannot register new user. An Username with name [{}] already exists".format(new_username)}, 409

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        insert_query = "INSERT INTO users VALUES (NULL, ?, ?)"
        result = cursor.execute(insert_query, (data['username'], data['password']))

        connection.commit()
        cursor.close()
        connection.close()

        return {'message':"User created successfully."}, 201
