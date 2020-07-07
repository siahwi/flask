from flask import jsonify, request
from flask_restful import Resource
from db_string import users
from helper import user_exist
import bcrypt


class Register(Resource):
    def post(self):
        posted_data = request.get_json()

        user_name = posted_data["username"]
        password = posted_data["password"]

        if user_exist(user_name):
            return_json = {
                "status": 301,
                "msg": "Invalid Username"
            }
            return jsonify(return_json)

        hashed_pw = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())

        users.insert({
            "user_name": user_name,
            "password": hashed_pw,
            "token": 10
        })

        return_json = {
            "status": 200,
            "msg": "You've successfully signed up to the API"
        }
        return jsonify(return_json)
