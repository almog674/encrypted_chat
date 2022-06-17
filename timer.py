from queue import Queue
import threading
import time

class Timer:
    def __init__(self, time_to_wait):
        self.time_to_wait = time_to_wait
        

    def start(self):
        global queue
        queue = Queue()
        time.sleep(self.time_to_wait)
        t = threading.Thread(target = self.over_time)
        t.start()
        t.join()
        return queue.deque()

    def over_time(self):
        queue.enque('Over')