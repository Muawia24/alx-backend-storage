#!/usr/bin/env python3
"""
5. Implementing an expiring web cache and tracker
"""
from functools import wraps
import requests
import redis
from typing import Callable

r = redis.Redis()


def cache(func: Callable) -> Callable:
    """
    decorator caching method
    """
    @wraps(func)
    def wrapper(url: str) -> str:
        """
         wrapper function for caching the output.
        """
        r.incr(f'count:{url}')

        cached_page = r.get(f'cache:{url}')
        if cached_page:
            return cached_page.decode('utf-8')

        response = func(url)
        r.set(f'count:{url}', 0)
        r.setex("cache:{}".format(url), 10, response)

        return response

    return wrapper


@cache
def get_page(url: str) -> str:
    """
    It uses the requests module to obtain the HTML content
    of a particular URL and returns it.
    rack how many times a particular URL was accessed in
    the key "count:{url}" and cache the result with an
    expiration time of 10 seconds.
    """
    return requests.get(url).text
