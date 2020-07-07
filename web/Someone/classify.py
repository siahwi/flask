from flask_restful import Resource
from flask import request, jsonify
from db_string import users
from helper import verify_credentials, generate_return_dictionary
import requests
import subprocess
import json


class Classify(Resource):
    def post(self):
        posted_data = request.get_json()
        user_name = posted_data["username"]
        password = posted_data["password"]
        ur = posted_data["url"]

        return_json, error = verify_credentials(user_name, password)
        print(return_json)
        if error:
            return return_json

        tokens = users.find({
            "user_name": user_name
        })[0]["token"]

        print("\n")
        print("\n")
        print(tokens)
        print("\n")


        if tokens <= 0:
            return generate_return_dictionary(303, "Not Enough Tokens ! ")

        r = requests.get(ur)
        return_json = {}
        with open("temp.jpg", "wb") as f:
            f.write(r.content)
            proc = subprocess.Popen(
                "python classify_image.py --model_dir=. --image_file=temp.jpg", shell=True)
            proc.communicate()[0]
            proc.wait()
            with open("text.txt") as g:
                return_json = json.load(g)

            users.update({
                "user_name": user_name
            }, {
                "$set": {
                    "token": tokens-1
                }
            })
        return return_json
