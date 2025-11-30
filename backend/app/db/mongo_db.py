from pymongo import MongoClient
from app.config import get_settings


MONGODB_URL = get_settings().MONGO_DB_URL

client = MongoClient(MONGODB_URL)
db = client.pdf_storage

