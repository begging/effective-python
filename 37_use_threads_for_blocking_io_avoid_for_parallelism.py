from time import time

'''
Although Python supports multiple threads of execution, the GIL causes only one
of them to make forward progress at a time.
'''
def factorize(number):
    for i in range(1, number + 1):
        if number % i == 0:
            yield i


numbers = [2139079, 1214759, 1516637, 1852285]
start = time()
for number in numbers:
    list(factorize(number))

end = time()
print('Took %.3f seconds' % (end - start))


'''
What’s surprising is that this takes even longer than running factorize in
serial.

There are ways to get CPython to utilize multiple cores, but it doesn’t work
with the standard Thread class.
'''
from threading import Thread

class FactorizeThread(Thread):
    def __init__(self, number):
        super().__init__()
        self.number = number

    def run(self):
        self.factors = list(factorize(self.number))


start = time()
threads = []
for number in numbers:
    thread = FactorizeThread(number)
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()

end = time()
print('Took %.3f seconds' % (end - start))
