# -*- coding: utf-8 -*-

import unittest
from random import random
from random import choice

from lru_cache import lru_cache


class LRUCacheTest(unittest.TestCase):

    def test_invocation(self):
        @lru_cache()
        def fn():
            return random()
        self.assertEqual(fn(), fn())

    def test_cache_clear(self):
        @lru_cache(maxsize=50)
        def f(x, y):
            return 7 * (x + y)

        choices = range(20)
        for i in range(500):
            f(choice(choices), choice(choices))
        f.clear()
        self.assertEqual((f.hits, f.misses), (0, 0))

    def test_cache_hits_nonzero(self):
        @lru_cache(maxsize=500)
        def f(x, y):
            return (x + y)

        choices = range(10)
        for i in range(5000):
            f(choice(choices), choice(choices))
        self.assertNotEqual(f.hits, 0)

    def test_cache_hits_zero(self):
        @lru_cache(maxsize=20)
        def f(x, y):
            return (x + y)

        choices = range(10000)
        for i in range(5000):
            f(choice(choices), choice(choices))
        self.assertEqual(f.hits, 0)

    def test_cache_miss_zero(self):
        @lru_cache(maxsize=500)
        def f(x, y):
            return x + y

        for i in range(10):
            f(2, 4)
        self.assertNotEqual(f.misses, 0)

    def test_cache_miss_nonzero(self):
        @lru_cache(maxsize=5)
        def f(x, y):
            return (x + y)

        choices = range(10)
        for i in range(50000):
            f(choice(choices), choice(choices))
        self.assertNotEqual(f.misses, 0)

    def test_unhashable_args(self):
        @lru_cache(maxsize=2)
        def findmax(iterable):
            return max(iterable)
        self.assertRaises(TypeError, findmax, [1, 2, 3, 5])

    def test_kwargs(self):
        @lru_cache(maxsize=5)
        def f(x, y, z):
            return (x + y) / z
        res = f(x=5, y=10, z=5)
        self.assertEqual(res, 3)

    def test_cache_refresh(self):
        @lru_cache(maxsize=5)
        def power_self(n):
            return n ** n
        # cache five results (five misses)
        for el in range(1, 6):
            power_self(el)

        # least used value replaced with new (six misses)
        power_self(8)

        # expecting previously computed result would cause cash miss
        power_self(1)
        self.assertEqual(power_self.misses, 7)

    def test_fromcache(self):
        @lru_cache()
        def factorial(n):
            return reduce(lambda x, y: x*y, xrange(1, n+1))

        factorial(5)
        factorial(5)
        self.assertEqual(factorial.hits, 1)




if __name__ == '__main__':
    unittest.main()
