from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from models.user import UserModel

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

        if UserModel.find_by_username(data['username']):
            return {'message': "Cannot register new user. An Username with name [{}] already exists".format(new_username)}, 409

        user = UserModel(data['username'], data['password'])
        user.save_to_db()

        return {'message':"User created successfully."}, 201
