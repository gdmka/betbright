# -*- coding: utf-8 -*-

from collections import OrderedDict
from functools import wraps

from logger import configure_logger

logging = configure_logger(filename="lru_cache.log",
                           logger_name="lru_cache")


def lru_cache(maxsize=100):
    """Last recently used cache implementation.

        Args:
            maxsize (int, default=100): maximum cache size

        Returns:
            Cached result or computed result of

        Properties:
            func.hits (int): number of cache hits.
            func.misses (int): number of cache misses.

        Bounded Methods:
            func.clear(): clear cache and reset hits/misses counter.

        Exception:
            If an exception will occur function will return None.
    """
    def decorating_fn(func):
        cache = OrderedDict()    # order: least recent to most recent

        @wraps(func)
        def wrapper(*args, **kwargs):
            key = args
            if kwargs:
                key += tuple(sorted(kwargs.items()))
            result = cache.get(key, None)
            if result:
                logging.info("Cache hit: {key}  {value}".format(key=key,
                                                                value=result))
                wrapper.hits += 1
            else:
                result = func(*args, **kwargs)
                logging.info("Cache miss: {key}  {value}".format(key=key,
                                                                 value=result))
                wrapper.misses += 1
            if len(cache) >= maxsize:
                cache.popitem(0)  # delete least used if cached limit reached
            cache[key] = result
            return result

        def clear():
            cache.clear()
            wrapper.hits = wrapper.misses = 0
            logging.info("Cache cleared.")

        wrapper.hits = wrapper.misses = 0
        wrapper.clear = lambda: clear()
        return wrapper
    return decorating_fn