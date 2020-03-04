def normalize(numbers):
    total = sum(numbers)
    result = []
    for value in numbers:
        percent = 100 * value / total
        result.append(percent)
    return result


'''
The normalize function above works when given a list.
'''
visits_list = [15, 35, 80]
percentages = normalize(visits_list)
print(percentages)


'''
The normalize function above doens't work when given an iterator.
Because iterators only work once.
'''
def read_visits_iter(arr):
    # Using a list arr instead of a data file
    for v in arr:
        yield int(v)

it = read_visits_iter(visits_list)
percentages = normalize(it)
print(percentages)


'''
Convert the iterator to a list.
This works, but the copy of the input iterator’s contents could be large.
'''
def normalize_copy(numbers):
    numbers = list(numbers) # copy the iterator
    total = sum(numbers)
    result = []
    for value in numbers:
        # Copy the iterator
        percent = 100 * value / total
        result.append(percent)
    return result

it = read_visits_iter(visits_list)
percentages = normalize_copy(it)
print(percentages)


'''
Though it works, having to pass a lambda function like this is clumsy.
'''
def normalize_func(get_iter):
    total = sum(get_iter()) # New iterator
    result = []
    for value in get_iter(): # New iterator
        percent = 100 * value / total
        result.append(percent)
    return result

percentages = normalize_func(lambda: read_visits_iter(visits_list))
print(percentages)


'''
Define an iterable container class. It will be more clear.
'''
class ReadVisits(object):
    # Using a list arr instead of a data file
    def __init__(self, arr):
        self.arr = arr

    def __iter__(self):
        for v in self.arr:
            yield int(v)

read_visit_instance = ReadVisits(visits_list)
percentages = normalize(read_visit_instance)
print(percentages)


'''
The protocol states that When an iterator is passed to the iter built-in
function, iter will return the iterator itself.

In contrast, when a container type is passed to iter, a new iterator object
will be returned each time.

You must not input an iterator to the normalize function. Because it will be
operated only once. Thus, you must input a contanier.

You can check if an input value is a container using iter built-in function.
'''
def normalize_defensive(numbers):
    if iter(numbers) is iter(numbers): # An iterator — bad!
        raise TypeError('Must supply a container')

    total = sum(numbers)
    result = []
    for value in numbers:
        percent = 100 * value / total
        result.append(percent)
    return result

visits_list = [15, 35, 80]
normalize_defensive(visits_list) # works

read_visit_instance = ReadVisits(visits_list)
normalize_defensive(read_visit_instance) # works

it = iter(visits_list)
normalize_defensive(it) # raise Error
