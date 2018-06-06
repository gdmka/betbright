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
            TypeError: if calling function arguments are not hashable.
    """
    def decorating_fn(func):
        cache = {}

        # Using OrderedDict approach
        # # https://github.com/python/cpython/blob/master/Lib/collections/__init__.py#L88
        PREV, NEXT, KEY, RES = 0, 1, 2, 3
        root = []
        root[:] = [root, root, None, None]

        @wraps(func)
        def wrapper(*args, **kwargs):
            key = args
            if not hasattr(key, "__hash__"):
                logging.error("Unhashable object: {}".format(key))
                raise TypeError("Unhashable objects are not supported")

            if kwargs:
                kwargs_list = []
                for item in sorted(kwargs.items()):
                    if not hasattr(item, "__hash__"):
                        logging.error("Unhashable object: {}".format(key))
                        raise TypeError("Unhashable objects are not supported")
                    kwargs_list.append(item)
                key += tuple(kwargs_list)

            link = cache.get(key, None)

            if link:
                link_prev, link_next, _key, result = link
                logging.info("Cache hit: {key}  {value}".format(key=_key,
                                                                value=result))
                link_prev[NEXT] = link_next
                link_next[PREV] = link_prev
                last = root[PREV]
                last[NEXT] = root[PREV] = link
                link[PREV] = last
                link[NEXT] = root
                wrapper.hits += 1
                return result

            else:
                result = func(*args, **kwargs)

                if len(cache) >= maxsize:
                    old_prev, old_next, old_key, old_value = root[NEXT]
                    root[NEXT] = old_next
                    old_next[PREV] = root
                    del cache[old_key], old_key, old_value
                last = root[PREV]
                link = [last, root, key, result]
                cache[key] = last[NEXT] = root[PREV] = link

                logging.info("Cache miss: {key}  {value}".format(key=key,
                                                                 value=result))
                wrapper.misses += 1
                return result

        def clear():
            cache.clear()
            wrapper.hits = wrapper.misses = 0
            logging.info("Cache cleared.")

        wrapper.hits = wrapper.misses = 0
        wrapper.clear = lambda: clear()
        return wrapper
    return decorating_fn
