#!/usr/bin/env python3
""" 0. Writing strings to Redis """
import redis
from typing import Union, Callable, Any
import uuid
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """
     count how many times methods of the Cache class are
     called.
    """
    @wraps(method)
    def counter(self, *args, **kwargs) -> Any:
        """
        wrapper method
        """
        if isinstance(self._redis, redis.Redis):
            self._redis.incr(method.__qualname__)

        return method(self, *args, **kwargs)

    return counter


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

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        generate a random key (e.g. using uuid), store the
        input data in Redis using the random key and
        return the key.
        """
        rand_key = str(uuid.uuid4())
        self._redis.set(rand_key, data)

        return rand_key

    def get(self, key: str,
            fn: Callable = None,
            ) -> Union[str, bytes, int, float]:
        """
        Reading from Redis
        """
        value = self._redis.get(key)

        if fn is None:
            return value

        return fn(value)

    def get_str(self, key: str) -> str:
        """
        Return a string value from redis
        """
        return self.get(key, lambda x: x.decode("utf-8"))

    def get_int(self, key: str) -> int:
        """
         Return an integer value from redis
        """
        return self.get(key, lambda x: int(x))
