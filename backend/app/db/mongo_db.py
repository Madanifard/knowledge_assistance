from pymongo import MongoClient
from app.config import get_settings


MONGODB_URI = get_settings().MONGODB_URI


class MongoConnection:
    def __init__(self, uri=MONGODB_URI, db="pdf_db"):
        self.client = MongoClient(uri)
        self.db = self.client[db]

    def get_collection(self, name: str):
        return self.db[name]