# The Fibonacci Sequence
Often used to teach recursion, the Fibonacci sequence is usually considered an 'easy' problem. However, the fastest way to compute it is still very much an open problem. In this document, we will detail our own experimentation with it!

## The Recursion Method
```py
def fib(n: int) -> int:
    if n==0 or n==1:
        return n
    return fib(n-1)+fib(n-2)
```
- Simple, but effective
- Benchmark for 15 (expected 610): `0.00007s`
- Benchmark for 30 (expected 832040): `0.01s`
- Benchmark for 40 (expected 102334155): `11.5s`
<hr>

- Though it works, it has a time complexity of O(2^n), an obviously indesirable amount.

## The Addition Method
```py
def fib(n: int) -> int:
    results=[0,1]
    for _ in range(1, n):
        results.append(results[-1]+results[-2])
    return results[-1]
```
- Benchmark for 15: `0.0000046s`
- Benchmark for 40: `0.000007s`
- Benchmark for 100 (expected 354224848179261915075): `0.000013s`
- Benchmark for 10000 (expected in 10000.expected): `0.002`
- Benchmark for 100000 (expected in 100000.expected):
```py
Traceback (most recent call last):
  File "/home/werdl/coding/fibonacci/funcspeed.py", line 17, in <module>
    print(test(fib, [100000], 10))
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/werdl/coding/fibonacci/funcspeed.py", line 6, in test
    print(func(*args))
ValueError: Exceeds the limit (4300 digits) for integer string conversion; use sys.set_int_max_str_digits() to increase the limit
```
- After function call for sys (not included in time): `0.1873849391937256s`
<hr>

- A fast method! When we started getting these numbers we were questioning if we could go any faster...

## The Mathematical Method
This one will need some explaining. The Fibonacci sequence, like many things in nature and mathematics, is tied to the golden ratio (phi $\varphi$), expressed as the equation 
### $`\varphi=\frac{1+\sqrt{5}}{2}=1.618...`$
So, there is a formula for the nth element of the sequence using this fact. The fastest one is known as Bidet's formula, and the version we used is this:
### $`u_{n}=\frac{\varphi^n-(-\varphi)^{-n}}{\sqrt{5}}`$

The Python implementation revolves around what was originally rather an unreadable one-liner that we have since changed:
```py
value=(
        (pow(phi,n)-pow(-phi,-n))
        /
        (sqrt(5))
    ) 
```
The full function:
```py
from math import sqrt
def fib(n: int) -> int:
    phi=(1+sqrt(5))/2
    value=(
        (pow(phi,n)-pow(-phi,-n))
        /
        (sqrt(5))
    ) 
    return round(value)
```
- Benchmark for 15: `0.000007s`
- Benchmark for 10000: 
```py
Traceback (most recent call last):
  File "/home/werdl/coding/fibonacci/funcspeed.py", line 22, in <module>
    print(test(fib, [10000], 10))
          ^^^^^^^^^^^^^^^^^^^^^^
  File "/home/werdl/coding/fibonacci/funcspeed.py", line 7, in test
    print(func(*args))
          ^^^^^^^^^^^
  File "/home/werdl/coding/fibonacci/funcspeed.py", line 15, in fib
    (pow(phi,n)-pow(-phi,-n))
     ^^^^^^^^^^
OverflowError: (34, 'Numerical result out of range')

```
<hr>

Why have we stopped the benchmarks there? Because Python started getting it wrong. It was out by around 25%, and so although it was very fast, Python could not handle such a large integer. Even with imports from Python standard `math` library, we couldn't fix the problem.

The issue lay in the way that Python stores floating point numbers. It uses the `double` type of C, as specified in `IEEE 754-1985`, which uses 53 bits to store numbers. 

However, after a few Google searches and a little documentation reading, we had a solution.

## The Mathematical Method 2
Using the same formula as before, but this time with the addition of a library called [`mpmath`](http://mpmath.org), which instead of using Python's backend, it utilises the [Python binding](https://github.com/aleaxit/gmpy) of [`GMP`](https://gmplib.org/), a GNU library for arbitrary precision maths.
```py
import mpmath
mpmath.mp.prec # precision
mpmath.mp.dps # other digit precision stuff

mpmath.mpf # float
mpmath.mpi # int

mpmath.nprint # print large numbers
```
Here is the full version of the code:
```py
from mpmath import mpf, power as pow, sqrt
import mpmath
from math import ceil
def fib(n: int, accuracy: int = 1000) -> int:
        mpmath.mp.prec=accuracy
        mpmath.mp.dps=accuracy
        phi=mpf((mpf('1')+mpf(sqrt(5)))/mpf('2'))
        mn=mpf(n)
        value=mpf(
            (pow(phi,mn)-pow(-phi,-mn))
            /
            (sqrt(mpf('5')))
        )
        splitted=str(value).split(".")

        toprint=splitted[0]
        if int(splitted[1][0])>=5:
            new=str(int(toprint[-1])+1) # string immutability workaround
            new=toprint[:-1]+new
        else:
            new=toprint
        mpmath.nprint(value, len(splitted[0])) # whole number
        return value
```

- Benchmark for 1000 (in 1000.expected): `0.00008s`
- Benchmark for 10000: `0.0004s`
- Benchmark for 100000: `0.01s`
- Benchmark for 1000000 (1000000.expected): `0.2s`
- Benchmark for 10000000 (10000000.expected): `3.1s`
<hr>

At this point, you may be wondering how we could possibly get any faster. You also may be wondering how we know these numbers are correct (We verified as far as we could on [bigprimes.net](http://bigprimes.net), and they all (1000th, 10000th etc.) seem to end in 875. Based on our research we think it has to do with the [Pisano period](https://en.wikipedia.org/wiki/Pisano_period) and how that is correlated to the Fibonacci sequence).

## The Matrix Multiplication Method
$`\begin{matrix}
u_n = \begin{bmatrix}1 & 1 \\ 1 & 0\end{bmatrix}^n\begin{bmatrix}1 \\ 0\end{bmatrix}\\
\end{matrix}`$

Matrix multiplication is known online as the fastest. But right at the beginning of this document, we said it was _still very much an open problem_. This is because we still don't know the fastest method of matrix multiplication! Also, our tests seemed to show the previous method as faster with very large numbers, even when we reran both methods. So these two things mean the problem is technically as yet unsolved!

Ironically after the last attempt, the matrix method is this:
```py
import numpy as np
def fib(n: int) -> int:
    matrix=np.array([
        [1, 1],
        [1, 0]
    ], dtype=object)
    result_matrix=np.linalg.matrix_power(matrix, n-1)
    return result_matrix[0, 0]
```
- Benchmark for 1000: `0.00003s`
- Benchmark for 10000: `0.0002s`
- Benchmark for 100000: `0.0004s`
- Benchmark for 1000000: `0.16s`
- Benchmark for 10000000: `6.15s`. Maybe the complicated one was better?

## A closing note
Over this document, we have examined several methods. Our tests, however show no fully conclusive winner! I suppose perhaps, it depends on the size of $n$.

Also, when running the code snippets the timing may seem inaccurate. This is because the print calls become rather costly, and so we don't include them in the time.

We hope you enjoyed this document, so we'll see you next time!

## Contibutors:
- [werdl](http://github.com/werdl)
- [uimaxbai](http://github.com/uimaxbai)
