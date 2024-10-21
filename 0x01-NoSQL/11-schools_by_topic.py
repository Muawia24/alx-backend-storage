#!/usr/bin/env python3
""" Where can I learn Python? """
import pymongo


def schools_by_topic(mongo_collection, topic):
    """
    Python function that returns the list of school having
    a specific topic.
    """
    result = mongo_collection.find({"topics": topic})

    return list(result)
