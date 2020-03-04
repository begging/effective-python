import itertools as it

x = [1, 2, 3, 4, 5]
y = ['a', 'b', 'c']

print(list(zip(x, y)))
print(list(it.zip_longest(x, y)))
