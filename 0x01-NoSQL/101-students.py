#!/usr/bin/env python3
""" 14. Top students """
import pymongo


def top_students(mongo_collection):
    """
    Python function that returns all students sorted by
    average score.
    """
    average = 0
    students = mongo_collection.find()

    for student in students:
        total = 0
        count = 0
        for topic in student.get("topics", []):
            total += topic.get("score", 0)
            count += 1

        if count > 0:
            averageScore = total / count
        else:
            averageScore = 0

        mongo_collection.update_one(
                {"_id": student["_id"]},
                {"$set": {"averageScore": averageScore}}
                )
    result = mongo_collection.find().sort("averageScore", pymongo.DESCENDING)
    return result
