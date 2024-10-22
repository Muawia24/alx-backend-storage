#!/usr/bin/env python3
""" 12. Log stats """
from pymongo import MongoClient


client = MongoClient('mongodb://127.0.0.1:27017')
nginx_collection = client.logs.nginx

logs_count = nginx_collection.count_documents({})

print("{} logs".format(logs_count))

methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]

print("Methods:")

for method in methods:
    method_count = nginx_collection.count_documents({"method": method})

    print("    method {}: {}".format(method, method_count))

status_check = nginx_collection.count_documents({
            "method": "GET",
            "path": "/status"
            })

print("{} status check".format(status_check))
