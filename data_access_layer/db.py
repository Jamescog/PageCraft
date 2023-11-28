from pymongo import MongoClient, DESCENDING
from bson.objectid import ObjectId
import os


class DataBaseManager:
    def __init__(self) -> None:
        self.client = MongoClient(
            os.getenv("DB_URL"),
        )
        self.db = self.client[os.getenv("DB_NAME")]
        self.collection = self.db[os.getenv("DB_COLLECTION")]
        self.randomly_selected = self.db["randomly_selected"]
        self.todays = self.db["todays_selection"]

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

    def create_new_collection(self, name: str) -> None:
        self.db.create_collection(name)

    def get_selected(self) -> str:
        selected = list(self.randomly_selected.find())
        return [s["title"] for s in selected]

    def change_todays_selection(self) -> str:
        already_selected = list(self.get_selected())
        pipeline = pipeline = [{"$sample": {"size": 1}}]

        random_selection = list(self.collection.aggregate(pipeline))
        while random_selection[0]["title"] in already_selected:
            random_selection = list(
                self.collection.aggregate([{"$sample": {"size": 1}}])
            )
        self.randomly_selected.insert_one({"title": random_selection[0]["title"]})

        # delete the current todays selection and insert the new one
        self.todays.drop()
        self.todays.insert_one({"title": random_selection[0]["title"]})
        return random_selection[0]

    def get_todays_selection(self) -> str:
        title = self.todays.find_one()["title"]
        return self.get_one_by_title(title)

    def get_random(self) -> str:
        pipeline = [{"$sample": {"size": 1}}]
        random_selection = list(self.collection.aggregate(pipeline))
        return random_selection[0]

    def search(
        self, search_term: str, rating: float = 0.0, skip: int = 0, limit: int = 10
    ) -> list:
        result = (
            self.collection.find(
                {"$text": {"$search": search_term}, "rating": {"$gte": rating}}
            )
            .sort("rating", DESCENDING)
            .skip(skip)
            .limit(limit)
        )
        return list(result)

    def search_by_author(self, author_name: str) -> list:
        result = self.collection.find({"author": author_name})
        return list(result)

    def return_count(self) -> int:
        return self.collection.count_documents({})

    def __str__(self) -> str:
        return str(self.collection.find({}))

    def __repr__(self) -> str:
        return str(self.collection.find({}))
