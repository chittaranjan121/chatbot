import uuid
from datetime import datetime, timezone
from pymongo import DESCENDING
from db.mongo import get_collection

conversations = get_collection("conversations")
conversations.create_index([("last_interacted", DESCENDING)])

def now_utc():
    return datetime.now(timezone.utc)

def new_conversation_id():
    return str(uuid.uuid4())

def create_conversation(first_user_message: str):
    cid = new_conversation_id()
    ts = now_utc()

    doc = {
        "_id": cid,
        "last_interacted": ts,
        "messages": [
            {"role": "user", "content": first_user_message, "ts": ts}
        ]
    }
    conversations.insert_one(doc)
    return cid

def add_message(cid: str, role: str, content: str):
    ts = now_utc()
    conversations.update_one(
        {"_id": cid},
        {
            "$push": {"messages": {"role": role, "content": content, "ts": ts}},
            "$set": {"last_interacted": ts}
        }
    )

def get_conversation(cid: str):
    return conversations.find_one({"_id": cid})

def get_all_conversations():
    docs = conversations.find({}, {"messages": 0}).sort("last_interacted", DESCENDING)
    return list(docs)
