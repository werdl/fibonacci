# Very fast, but only prints out one number
from sys import setrecursionlimit,set_int_max_str_digits # See below for details
from time import time

setrecursionlimit(1000000)
set_int_max_str_digits(1000000)

def fib(n, computed = {0: 0, 1: 1}):
    if n not in computed:
        computed[n] = fib(n-1, computed) + fib(n-2, computed)
    return computed[n]


toRun = 123456
start_time = time()
print(fib(toRun))
print(f"--- {time() - start_time}s to go through {toRun} numbers ---")