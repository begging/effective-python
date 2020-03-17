'''
The initial call to next is required to prepare the generator for receiving the
first send by advancing it to the first yield expression.
'''
def my_coroutine():
    while True:
        received = yield
        print('Received:', received)

it = my_coroutine()
next(it)
it.send('First')
it.send('Second')



'''
The generator function will seemingly run forever, making forward progress with
each new call to send.
'''
def minimize():
    current = yield # get item from send function outside
    while True:
        value = yield current # get item from send function outside
        current = min(value, current)
        print('yield')

it = minimize()
next(it)
print(it.send(10))
print(it.send(4))
print(it.send(22))
print(it.send(-1))


'''
test coroutines
'''
def test():
    print('start test')
    a = yield
    print(a)
    b = yield
    print(b)
    c = yield
    print(c)


it = test()
next(it)
print(it.send('a'))
print(it.send('b'))
print(it.send('c'))
