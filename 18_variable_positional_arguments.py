def my_generator():
    for i in range(10):
        yield i

def my_func(*args):
    print(args)

it = my_generator()

'''
Problem 1: An iterator could consume a lot of memory if it's large.
'''
my_func(*it)
