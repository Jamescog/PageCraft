from pymongo import MongoClient
from bson.objectid import ObjectId
import os


class DataBaseManager:
    def __init__(self) -> None:
        self.client = MongoClient(os.getenv("DB_URL"))
        self.db = self.client[os.getenv("DB_NAME")]
        self.collection = self.db[os.getenv("DB_COLLECTION")]

    def get_one_by_title(self, title: str) -> dict:
        return self.collection.find_one({"title": title})

    def get_one_by_id(self, id: str) -> dict:
        return self.collection.find_one({"_id": ObjectId(id)})

    def get_all(self) -> list:
        return list(self.collection.find({}))

    def insert_one(self, data: dict) -> None:
        self.collection.insert_one(data)

    def insert_many(self, data: list) -> None:
        self.collection.insert_many(data)

    def get_many_by__in(self, titles: list) -> list:
        return list(self.collection.find({"title": {"$in": titles}}))

    def __str__(self) -> str:
        return str(self.collection.find({}))

    def __repr__(self) -> str:
        return str(self.collection.find({}))
