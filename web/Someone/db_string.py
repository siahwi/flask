from pymongo import MongoClient

client = MongoClient("mongodb://db:27017")
db = client.classifierDB
users = db["users"]
