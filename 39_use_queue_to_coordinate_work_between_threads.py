from collections import deque
from threading import Thread, Lock
from time import sleep
from queue import Queue

# class MyQueue:
#     def __init__(self):
#         self.items = deque()
#         self.lock = Lock()

#     def put(self, item):
#         with self.lock:
#             self.items.append(item)

#     def get(self):
#         with self.lock:
#             return self.items.popleft()


# class Worker(Thread):
#     def __init__(self, func, in_queue, out_queue):
#         super().__init__()
#         self.func = func
#         self.in_queue = in_queue
#         self.out_queue = out_queue
#         self.polled_count = 0
#         self.work_done = 0
#         self.error_count = 0

#     def run(self):
#         while True:
#             self.polled_count += 1
#             try:
#                 item = self.in_queue.get()
#             except IndexError:
#                 sleep(0.001) # No work to do
#                 self.error_count += 1
#             else:
#                 result = self.func(item)
#                 self.out_queue.put(result)
#                 self.work_done += 1

# def download(item):
#     return object()

# def resize(item):
#     return object()

# def upload(item):
#     return object()

# download_queue = MyQueue()
# resize_queue = MyQueue()
# upload_queue = MyQueue()
# done_queue = MyQueue()
# threads = [
#     Worker(download, download_queue, resize_queue),
#     Worker(resize, resize_queue, upload_queue),
#     Worker(upload, upload_queue, done_queue)
# ]

# for thread in threads:
#     thread.start()

# for _ in range(1000):
#     download_queue.put(object())

# while len(done_queue.items) < 1000:
#     # print(len(done_queue.items))
#     pass

# processed = len(done_queue.items)
# polled = sum(t.polled_count for t in threads)
# sum_error_count = sum(t.error_count for t in threads)
# print('Processed', processed, 'items after polling', polled, 'times')
# print('error_count', sum_error_count)


# queue = Queue()

# def consumer():
#     print('Consumer waiting')
#     queue.get() # Runs after put() below
#     print('Consumer done')

# thread = Thread(target=consumer)
# thread.start()

# print('Producer putting')
# queue.put(object())
# thread.join()
# print('Producer done')


# '''
# '''
# queue = Queue(1) # Buffer size of 1
# def consumer():
#     sleep(1) # wait
#     queue.get() # Runs second
#     print('Consumer got 1')
#     queue.get() # Runs fourth
#     print('Consumer got 2')

# thread = Thread(target=consumer)
# thread.start()

# queue.put(object())
# print('Producer put 1')
# queue.put(object())
# print('Producer put 2')
# thread.join()
# print('Producer done')


in_queue = Queue()

def consumer():
    print('Consumer waiting')
    work = in_queue.get()
    print('Consumer working')
    # Doing work
    # …
    print('Consumer done')
    in_queue.task_done()

Thread(target=consumer).start()

in_queue.put(object())
print('Producer waiting')
in_queue.join()
print('Producer done')
'''
Closable Queue / Stoppable Thread
'''
class ClosableQueue(Queue):
    SENTINEL = object()

    def close(self):
        self.put(self.SENTINEL)

    def __iter__(self):
        while True:
            item = self.get()
            try:
                if item is self.SENTINEL:
                    return # Cause the thread to exit
                yield item

            finally:
                self.task_done()


class StoppableWorker(Thread):
    def __init__(self, func, in_queue, out_queue):
        super().__init__()
        self.func = func
        self.in_queue = in_queue
        self.out_queue = out_queue

    def run(self):
        for item in self.in_queue:
            result = self.func(item)
            self.out_queue.put(result)

download_queue = ClosableQueue()
resize_queue = ClosableQueue()
upload_queue = ClosableQueue()
done_queue = ClosableQueue()
threads = [
    StoppableWorker(lambda x: object(), download_queue, resize_queue),
    StoppableWorker(lambda x: object(), resize_queue, upload_queue),
    StoppableWorker(lambda x: object(), upload_queue, done_queue)
]

for thread in threads:
    thread.start()

for _ in range(1000):
    download_queue.put(object())

download_queue.close()
download_queue.join()
resize_queue.close()
resize_queue.join()
upload_queue.close()
upload_queue.join()
print(done_queue.qsize(), 'items finished')
