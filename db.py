from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["rag_app"]

users_collection = db["users"]
chat_collection = db["chats"]