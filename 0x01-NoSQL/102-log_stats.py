#!/usr/bin/env python3
""" 12. Log stats """
from pymongo import MongoClient


def log_stats():
    """
     Python script that provides some stats about Nginx
     logs stored in MongoDB.
    """
    client = MongoClient('mongodb://127.0.0.1:27017')
    nginx_collection = client.logs.nginx

    logs_count = nginx_collection.count_documents({})

    print("{} logs".format(logs_count))

    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]

    print("Methods:")

    for method in methods:
        method_count = nginx_collection.count_documents({"method": method})

        print("\tmethod {}: {}".format(method, method_count))

    status_check = nginx_collection.count_documents({
            "method": "GET",
            "path": "/status"
            })

    print("{} status check".format(status_check))

    top_ips = nginx_collection.aggregate(
            [
                {"$group": {
                    "_id": "$ip",
                    "count": {"$sum": 1}
                    }},
                {"$sort": {"count": -1}},

                {"$limit": 10}
                ]
            )

    for ip in top_ips:
        print("\t{}: {}".format(ip["_id"], ip["count"]))


if __name__ == "__main__":
    log_stats()
