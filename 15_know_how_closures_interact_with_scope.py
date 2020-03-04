'''
a normal closure function
'''
def sort_priority(values, group):
    def helper(x):
        if x in group:
            return (0, x)
        return (1, x)
    values.sort(key=helper)


'''
a closure function which has a local variable
'''
def sort_priority2(values, group):
    found = False
    def helper(x):
        if x in group:
            found = True # This doesn't affect above 'found' variable
            return (0, x)
        return (1, x)
    values.sort(key=helper)
    return found

numbers = [8, 3, 1, 2, 5, 4, 7, 6]
group = {2, 3, 5, 7}
found = sort_priority2(numbers, group)
print('Found:', found) # False
print(numbers)


'''
a closure function which uses nonlocal keyword
'''
def sort_priority3(values, group):
    found = False
    def helper(x):
        nonlocal found
        if x in group:
            found = True # This affects above 'found' variable
            return (0, x)
        return (1, x)
    values.sort(key=helper)
    return found

numbers = [8, 3, 1, 2, 5, 4, 7, 6]
group = {2, 3, 5, 7}
found = sort_priority3(numbers, group)
print('Found:', found) # True
print(numbers)


'''
Using a helper class
    - much easier to read
'''
class Sorter(object):
    def __init__(self, group):
        self.group = group
        self.found = False

    def __call__(self, x):
        if x in self.group:
            self.found = True
            return (0, x)
        return (1, x)

numbers = [8, 3, 1, 2, 5, 4, 7, 6]
group = {2, 3, 5, 7}
sorter = Sorter(group)
numbers.sort(key=sorter)
print('Found:', sorter.found) # True
print(numbers)



'''
Python2 doesn't support the nonlocal keyword
This is the alternative way in Python2
'''
def sort_priority(numbers, group):
    found = [False]
    def helper(x):
        if x in group:
            found[0] = True
            return (0, x)
        return (1, x)
    numbers.sort(key=helper)
    return found[0]
