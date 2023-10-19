## Bidet's formula in Python
```py
(
    (phi**n--phi**-n)
    /
    (sqrt(5))
) 
```
- A wrapper around this
### But why Python... its so slow
- I agree, but...
- `mpmath`
- A python library that does big numbers well, and _very_ precisely

### Ok, so its fast. How fast?
#### Excluding the print statement, only Bidet's formula
- 1000th element of sequence took on average `0.00035419702529907224s`
- 10000th element - `0.012049508094787598`
- 100000th element - `0.6693078279495239s`
- I'm pretty happy with the speed!