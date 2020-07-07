import bcrypt
from flask import jsonify
from db_string import users


def user_exist(user_name):
    if users.find({"user_name": user_name}).count() == 0:
        return False
    else:
        return True


def verify_password(user_name, password):
    if not user_exist(user_name):
        return False
    hashed_pw = users.find({
        "user_name": user_name
    })[0]["password"]

    if bcrypt.hashpw(password.encode('utf8'), hashed_pw) == hashed_pw:
        return True
    else:
        return False


def count_tokens(user_name):
    tokens = users.find({
        "user_name": user_name
    })[0]["token"]
    return tokens

def generate_return_dictionary(status, msg):
    return_json = {
        "status": status,
        "msg": msg
    }
    return jsonify(return_json)


def verify_credentials(user_name, password):
    if not user_exist(user_name):
        return generate_return_dictionary(301, "Invalid Username"), True
    correct_pw = verify_password(user_name, password)
    if not correct_pw:
        return generate_return_dictionary(302, "Invalid Password"), True
    return None, False
