from django.shortcuts import render
from bson import ObjectId
import os
from pymongo import MongoClient
from datetime import datetime

MONGO_DB_URI_TEMPLATE = os.getenv("MONGO_DB_URI_TEMPLATE")
mongo_client = MongoClient(MONGO_DB_URI_TEMPLATE, tls=True)

db = mongo_client["questionBank"]
answered_collection = db["answered_questions"]


# Create your views here.
def fetch_unanswered_question(username: str, question_limit: int):
    try:
        answered_questions = answered_collection.find_one({"username": username})
        answered_ids = answered_questions["answered_ids"] if answered_questions else []

        if len(answered_ids) >= question_limit:
            return {"error": "Questions limit reached", "status": 409}

        answered_ids = [
            ObjectId(answered_id.get("question_id")) for answered_id in answered_ids
        ]
        pipeline = [
            {
                "$match": {
                    "_id": {"$nin": answered_ids},
                    "test_id": username.split("_")[0] + "_",
                }
            },
            {"$sample": {"size": 1}},
        ]
        question_cursor = collection.aggregate(pipeline)
        question = next(question_cursor, None)

        if question:
            return {
                "question_id": str(question["_id"]),
                "text": question["question_text"],
                "options": question["options"],
            }
    except KeyError:
        return {}
    return None


def record_answered_question(username, question_id):
    answered_questions = answered_collection.find_one({"username": username})
    if answered_questions:
        answered_ids = answered_questions["answered_ids"]
        if not any(answer["question_id"] == question_id for answer in answered_ids):
            answered_ids.append(
                {"question_id": question_id, "timestamp": datetime.utcnow()}
            )
            answered_collection.update_one(
                {"username": username}, {"$set": {"answered_ids": answered_ids}}
            )
    else:
        answered_collection.insert_one(
            {
                "username": username,
                "answered_ids": [
                    {"question_id": question_id, "timestamp": datetime.utcnow()}
                ],
            }
        )
