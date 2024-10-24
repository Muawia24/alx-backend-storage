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
        key = "count:{}".format(url)
        r.incr(key)

        cached_page = r.get("cache:{}".format(url))
        if cached_page:
            return cached_page.decode('utf-8')

        r.set(key, 0)
        response = func(url)
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
    response = requests.get(url)
    if response.status_code == 200:
        html = response.text
    else:
        html = None

    return html
