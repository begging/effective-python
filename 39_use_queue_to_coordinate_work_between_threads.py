from collections import deque
from threading import Thread, Lock
from time import sleep

class MyQueue:
    def __init__(self):
        self.items = deque()
        self.lock = Lock()

    def put(self, item):
        with self.lock:
            self.items.append(item)

    def get(self):
        with self.lock:
            return self.items.popleft()


class Worker(Thread):
    def __init__(self, func, in_queue, out_queue):
        super().__init__()
        self.func = func
        self.in_queue = in_queue
        self.out_queue = out_queue
        self.polled_count = 0
        self.work_done = 0
        self.error_count = 0

    def run(self):
        while True:
            self.polled_count += 1
            try:
                item = self.in_queue.get()
            except IndexError:
                sleep(0.001) # No work to do
                self.error_count += 1
            else:
                result = self.func(item)
                self.out_queue.put(result)
                self.work_done += 1

def download(item):
    return object()

def resize(item):
    return object()

def upload(item):
    return object()

download_queue = MyQueue()
resize_queue = MyQueue()
upload_queue = MyQueue()
done_queue = MyQueue()
threads = [
    Worker(download, download_queue, resize_queue),
    Worker(resize, resize_queue, upload_queue),
    Worker(upload, upload_queue, done_queue)
]

for thread in threads:
    thread.start()

for _ in range(1000):
    download_queue.put(object())

while len(done_queue.items) < 1000:
    # print(len(done_queue.items))
    pass

processed = len(done_queue.items)
polled = sum(t.polled_count for t in threads)
sum_error_count = sum(t.error_count for t in threads)
print('Processed', processed, 'items after polling', polled, 'times')
print('error_count', sum_error_count)
