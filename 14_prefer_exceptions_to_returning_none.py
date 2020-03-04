
######## Bad case 1 ##########
def divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return None

x, y = 5, 0
result = divide(x, y)
if result is None:
    print('Invalid inputs')



######## Good case 1 ##########
def divide(a, b):
    try:
        return True, a / b
    except ZeroDivisionError:
        return False, None

x, y = 5, 0
success, result = divide(x, y)
if not success:
    print('Invalid inputs')



######## Good case 2 ##########
def divide(a, b):
    '''
    Instead of returing None, raise an Exception to make caller deal with it.
    '''
    try:
        return a / b
    except ZeroDivisionError as e:
        raise ValueError('nvalid inputs') from e

x, y = 5, 2
try:
    result = divide(x, y)
except ValueError:
    print('Invalid inputs')
else:
    print('Result is %.1f' % result)
