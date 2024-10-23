#!/usr/bin/env python3
""" 0. Writing strings to Redis """
import redis
from typing import Union
import uuid


class Cache:
    """
    Writing strings to Redis
    """

    def __init__(self):
        """
        store an instance of the Redis client as a private
        variable named _redis
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        generate a random key (e.g. using uuid), store the
        input data in Redis using the random key and
        return the key.
        """
        rand_key = str(uuid.uuid4())
        self._redis.set(rand_key, data)

        return rand_key
