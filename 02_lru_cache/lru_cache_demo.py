# -*- coding: utf-8 -*-

import profile
import argparse

from lru_cache import lru_cache


parser = argparse.ArgumentParser()
parser.add_argument("mode")
args = parser.parse_args()

"""To Compute 25th Fibonacci number using lru_cache:
    
    * python lru_cache_demo.py cache
   To Compute 25th number without caching
    *  python lru_cache_demo.py naive
    
   profile module takes care of showing the call stats and execution time. 
"""


@lru_cache()
def fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n - 1) + fib(n - 2)


def fib_seq(n):
    seq = []
    if n > 0:
        seq.extend(fib_seq(n - 1))
    seq.append(fib(n))
    return seq


def fib_naive(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib_naive(n - 1) + fib_naive(n - 2)


def fib_seq_naive(n):
    seq = []
    if n > 0:
        seq.extend(fib_seq_naive(n - 1))
    seq.append(fib_naive(n))
    return seq


if __name__ == '__main__':
    if args.mode == "lru":
        profile.run('print(fib_seq(25)); print()')
    if args.mode == "naive":
        profile.run('print(fib_seq_naive(25)); print()')
