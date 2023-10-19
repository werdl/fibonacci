"""
Note - pow() is used as it is around twice as fast as **,
at least in my benchmarking.

A note on the formula used and floating-point accuracy.

Computers are not infallible, they can only go so far.
With large values of n (for fib(n)), the values will be off.
This owes to the way your computer works under the PC case, if you will.
With Python (really C's) double precision floating-point type,
with large values it will falter.
When I say double precision, more info can be found at IEEE 754-1985.

This fixes most of those issues! Wahey!
"""

from mpmath import power as pow, mpf, sqrt, mpi, log10
import mpmath
import time
import sys

def OneOrZero(prompt, fail):
    """
    Returns one or zero.
    `prompt` is the prompt to input()
    `fail` is the message displayed upon failure
    """
    inp=input(prompt)
    try:
        x=int(inp)
        if x!=1 and x!=0:
            raise ValueError
        return x
    except ValueError:
        print(fail)
        OneOrZero(prompt,fail)
class Fibonacci:
    def __init__(self):
        self.table=[]
        mpmath.mp.prec=100
        mpmath.mp.dps=100

    @classmethod
    def gen_table(self, n: int) -> list:
        """
        Generate a table of values for Fibonacci numbers up to n
        """
        if "table" not in dir(self): # allows for calling on Fibonacci class or object
            self.table=[]
        self.table.append(0)
        self.table.append(1)
        for _ in range(2,n):
            self.table.append(self.table[-1]+self.table[-2])
        return self.table
   
    @classmethod
    def nth(self, n: int, accuracy: int = 1000) -> int:
        if accuracy>650:
            sys.set_int_max_str_digits(accuracy+10)
        mpmath.mp.prec=accuracy # we set these to the same value, but they
        mpmath.mp.dps=accuracy  # should be different, but
        phi=mpf((mpf('1')+mpf(sqrt('5')))/mpf('2'))
        start=time.time()
        value=mpf(
            (pow(phi,mpf(n))-pow(-phi,-mpf(n)))
            /
            (sqrt(mpf('5')))
        ) # generated value
        end=time.time()
        splitted=str(value).split(".")

        toprint=splitted[0]
        if int(splitted[1][0])>=5: # check if we should round
            new=str(int(toprint[-1])+1) # string immutability workaround
            new=toprint[:-1]+new
        else:
            new=toprint
        mpmath.nprint(value, len(splitted[0])) # whole number
        return (value,end-start)
   
    @classmethod
    def is_fib(self, n: int):
        if float(5*n+4).is_integer():
            return True
        elif float(5*n-4).is_integer():
            return True
        else:
            return False

max_n=int(input("Please enter the term number of the number you want: "))
if not OneOrZero("Would you like a list (0) or the term (1)? ",
                 "Please enter a value that is either 0 or 1."):
    start_table=time.time()
    result=Fibonacci.gen_table(max_n)
    end_table=time.time()
    print(str(result).replace("'","").replace("[","").replace("]",""))
    print(f"That that took {end_table-start_table}s")
else:
    start_raw=time.time()
    result=Fibonacci.nth(max_n, max_n)
    end_raw=time.time()
    print(f"That that took {result[1]}s to do the actual maths, and \
{end_raw-start_raw}s overall")

