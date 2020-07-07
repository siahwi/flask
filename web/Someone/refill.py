from flask import jsonify, request
from helper import user_exist, count_tokens
from flask_restful import Resource
from db_string import users

class Refill(Resource):
    def post(self):
        posted_data = request.get_json()

        user_name = posted_data["username"]
        password = posted_data["admin_pw"]
        refill_amount = posted_data["refill"]

        if refill_amount <= 0:
            return_json = {
                "status": 305,
                "msg": "Invalid refill_token_count"
            }
            return jsonify(return_json)

        if not user_exist(user_name):
            return_json = {
                "status": 301,
                "msg": "Invalid Username"
            }
            return jsonify(return_json)

        correct_pw = "abc123"
        if not password == correct_pw:
            return_json = {
                "status": 304,
                "msg": "invalid admin"
            }
            return jsonify(return_json)

        current_tokens = count_tokens(user_name)

        users.update({
            "user_name": user_name
        }, {
            "$set": {
                "token": refill_amount+current_tokens
            }
        })
        return_json = {
            "status": 200,
            "msg": "Refilled Successfully"
        }
        return jsonify(return_json)
