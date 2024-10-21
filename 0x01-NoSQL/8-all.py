#!/usr/bin/env python3
"""  List all documents in Python """
import pymongo


def list_all(mongo_collection):
    """
    Python function that lists all documents in
    a collection.
    """
    return [doc for doc in mongo_collection.find()]
