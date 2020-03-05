'''
The * symbol in the argument list indicates the end of positional arguments and
the beginning of keyword-only arguments.
'''
def safe_division_c(number, divisor, *,
                    ignore_overflow=False,
                    ignore_zero_division=False):

    try:
        return number / divisor
    except OverflowError:
        if ignore_overflow:
            return 0
        else:
            raise
    except ZeroDivisionError:
        if ignore_zero_division:
            return float('inf')
        else:
            raise

s1 = safe_division_c(1, 10**500, ignore_overflow=True) # works
print(s1)

s2 = safe_division_c(1, 0, ignore_zero_division=True) # works
print(s2)

try:
    f1 = safe_division_c(1, 10**500, True, False) # doesn't work
except TypeError as e:
    print(e)



'''
Python2 doesn't have explicit syntax for specifying keyword-only arguments.

'''
def safe_division_d(number, divisor, **kwargs):

    ignore_overflow = kwargs.pop('ignore_overflow', False)
    ignore_zero_division = kwargs.pop('ignore_zero_division', False)
    if kwargs:
        raise TypeError('Unexpected **kwargs: %r' % kwargs)

    try:
        return number / divisor
    except OverflowError:
        if ignore_overflow:
            return 0
        else:
            raise
    except ZeroDivisionError:
        if ignore_zero_division:
            return float('inf')
        else:
            raise

print(safe_division_d(1, 0, ignore_zero_division=True))
print(safe_division_d(1, 10**500, ignore_overflow=True))
print(safe_division_d(1, 0))
