#!/usr/bin/env python3
""" 0. Writing strings to Redis """
import redis
from typing import Union, Callable, Any
import uuid
from functools import wraps


def replay(func: Callable) -> None:
    """
     display the history of calls of a particular function.
    """
    if func is None or not hasattr(func, '__self__'):
        return

    redis_store = getattr(func.__self__, '_redis', None)
    if not isinstance(redis_store, redis.Redis):
        return

    fn_name = func.__qualname__
    ins = "{}:inputs".format(fn_name)
    outs = "{}:outputs".format(fn_name)

    fn_count = 0
    if redis_store.exists(fn_name) != 0:
        fn_count = int(redis_store.get(fn_name))

    print("{} was called {} times:".format(fn_name, fn_count))
    ins_list = redis_store.lrange(ins, 0, -1)
    outs_list = redis_store.lrange(outs, 0, -1)

    for key, value in zip(ins_list, outs_list):
        print("{}(*{}) -> {}".format(fn_name, key.decode("utf-8"), value))


def call_history(method: Callable) -> Callable:
    """
     store the history of inputs and outputs for a
     particular function.
    """
    @wraps(method)
    def push(self, *args, **kwargs) -> Any:
        """
        Returns the method's output after storing its
        inputs and output.
        """
        ins = "{}:inputs".format(method.__qualname__)
        outs = "{}:outputs".format(method.__qualname__)
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(ins, str(args))
        output = method(self, *args, **kwargs)

        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(outs, output)

        return output

    return push


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

    @call_history
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
