#!/usr/bin/env python3
""" Main file """

cache = __import__('web').get_page



print(cache("http://slowwly.robertomurray.co.uk/delay/5000/url/http://www.example.com"))
