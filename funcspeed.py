import time, sys
from math import sqrt, pow
def test(func, args, howmany=10) -> int:
    total=0
    for i in range(howmany):
        start=time.time()
        func(*args)
        end=time.time()
        total+=end-start
    return total/howmany

import numpy as np
def fib(n: int) -> int:
    matrix=np.array([
        [1, 1],
        [1, 0]
    ], dtype=object)
    result_matrix=np.linalg.matrix_power(matrix, n-1)
    return result_matrix[0, 0]

sys.set_int_max_str_digits(10000000)
torun=10_000_000
print(test(fib, [torun], 1))