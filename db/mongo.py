from pymongo import MongoClient
import config.settings as settings

_client = MongoClient(settings.MONGO_URL, tz_aware=True)
_db = _client[settings.MONGO_DB]

def get_collection(name: str):
    return _db[name]
