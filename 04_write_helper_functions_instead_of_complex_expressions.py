from urllib.parse import parse_qs
my_values = parse_qs('red=5&blue=0&green=', keep_blank_values=True)
print(repr(my_values))

'''
This expression below is difficult to read.

Python’s syntax makes it all too easy to write single-line expressions that are
overly complicated and difficult to read.
'''
red = my_values.get('red', [''])[0] or 0
green = my_values.get('green', [''])[0] or 0
opacity = my_values.get('opacity', [''])[0] or 0
print('Red: %r' % red)
print('Green: %r' % green)
print('Opacity: %r' % opacity)


'''
This is better.
But still not as clear as the alternative of a full if/else statement over
multiple lines.
'''
red = my_values.get('red', [''])
red = int(red[0]) if red[0] else 0



'''
The if/else expression provides a more readable alternative to using Boolean
operators like or and and in expressions.
'''
green = my_values.get('green', [''])
if green[0]:
    green = int(green[0])
else:
    green = 0


'''
Writing a helper function is the way to go, especially if you need to use this
logic repeatedly.

But Seeing all of the logic spread out like this makes the dense version seem
even more complex.
'''
def get_first_int(values, key, default=0):
    found = values.get(key, [''])
    if found[0]:
        found = int(found[0])
    else:
        found = default

    return found
