# -*- coding: utf-8 -*-

import urllib.parse
from utils.redirect import perform_redirect

def query_arg(fn):
    def wrapped(*args, query = None, **kwargs):
        if query is None:
            return fn(*args, **kwargs)
        else:
            return fn(*args, query = Query(query), **kwargs)
    return wrapped

def valid_query_arg(redirect_url):
    def decorator(fn):
        @query_arg
        def wrapped(*args, query = None, **kwargs):
            if query is None or not query.is_valid():
                perform_redirect(redirect_url)
            else:
                return fn(*args, query = query, **kwargs)
        return wrapped
    return decorator

# Internal module function.
def force_valid(fn):
    def wrapped(self, *args, **kwargs):
        if not self.is_valid():
            raise Exception('Query is not valid.')
        else:
            return fn(self, *args, **kwargs)
    return wrapped

class Query():
    def __init__(self, query):
        self.__url_safe_mode = True
        if not query:
            self.__valid = False
        else:
            query = urllib.parse.unquote_plus(query)
            self.__valid = True
            self.__query = query
            self.__keyword = query.split()[0]

    def is_valid(self):
        return self.__valid

    @force_valid
    def keyword(self):
        return self.__keyword

    @force_valid
    def body(self):
        return self.__be_safe(self.__query[len(self.__keyword) + 1:])

    @force_valid
    def __str__(self):
        return self.__be_safe(self.__query)

    @force_valid
    def url_unsafe(self):
        # str() to force quote_plus so constructor doesn’t unquote the string
        # twice.
        unsafe = Query(str(self))
        unsafe.__url_safe_mode = False
        return unsafe

    # Unlike str(X) x.to_str() can be used in templates.
    @force_valid
    def to_str(self):
        return str(self)

    def __be_safe(self, string):
        if self.__url_safe_mode:
            return urllib.parse.quote_plus(string)
        else:
            return string
