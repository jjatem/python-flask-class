import sqlite3
from db import db

class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

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
