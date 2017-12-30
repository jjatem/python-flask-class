import sqlite3
from flask import Flask, request
from flask_restful import Resource, Api, reqparse

class User:
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    def __str__(self):
        return "UserId={}, Username={}, Password={}.".format(self.id, self.username, self.password)

    @classmethod
    def find_by_username(cls, username):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        select_query = "SELECT * FROM users WHERE username = ?"
        result = cursor.execute(select_query, (username,))

        row = result.fetchone()

        if row is not None:
            user = cls(*row)
        else:
            user = None

        cursor.close()
        connection.close()
        return user

    @classmethod
    def find_by_userid(cls, user_id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        select_query = "SELECT * FROM users WHERE id = ?"
        result = cursor.execute(select_query, (user_id,))

        row = result.fetchone()

        if row is not None:
            user = cls(*row)
        else:
            user = None

        cursor.close()
        connection.close()
        return user
#test code => u = User.find_by_username("joffre") print(u)

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

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        insert_query = "INSERT INTO users VALUES (NULL, ?, ?)"
        result = cursor.execute(insert_query, (data['username'], data['password']))

        connection.commit()
        cursor.close()
        connection.close()

        return {'message':"User created successfully."}, 201
