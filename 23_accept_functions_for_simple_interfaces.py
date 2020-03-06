from collections import defaultdict

def increment_with_report(current, increments):
    added_count = 0

    def missing():
        nonlocal added_count
        added_count += 1
        return 0

    result = defaultdict(missing, current)

    for key, amount in increments:
        result[key] += amount

    return result, added_count

current = {'green': 12, 'blue':3}
increments = [('red', 5),
              ('blue', 17),
              ('orange', 9),]

result, added_count = increment_with_report(current, increments)
print(result.items())
print(added_count)



'''
The function above is hard to understand because of the closure function.
Another approach is to define a small helper class.
'''
class CountMissing:
    def __init__(self):
        self.added = 0

    def missing(self):
        self.added += 1
        return 0

counter = CountMissing()
result = defaultdict(counter.missing, current)
for key, amount in increments:
    result[key] += amount

print(result.items())
print(added_count)



'''
The helper class above is clearer than the increment_with_report function.

However, until you see its usage, it's still not immediately obvious what the
purpose of the CountMissing class is.

To clarify this situation, Python allows classes to define the __call__ method.
__call__ allows an object to be called just like a function.

It directs new readers of the code to the entry point that’s responsible for
the class’s primary behavior.
'''
class CountMissing:
    def __init__(self):
        self.added = 0

    def __call__(self):
        self.added += 1
        return 0

counter = CountMissing()
result = defaultdict(counter, current)
for key, amount in increments:
    result[key] += amount

print(result.items())
print(added_count)
