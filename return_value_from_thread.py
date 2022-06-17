import time
import threading



global queue

class Queue(object):
    def __init__(self):
        self.item = []

    def __repr__(self):
        return '{}'.format(self.item)

    def __str__(self):
        return '{}'.format(self.item)
    
    def enque(self, add):
        self.item.insert(0, add)
        return True
    
    def size(self):
        return len(self.item)

    def isempty(self):
        if self.size() == 0:
            return True
        else:
            return False

    def deque(self):
        if self.size() == 0:
            return None
        else:
            return self.item.pop()


queue = Queue()

def some_foo(num):
    print('Working on it...')
    time.sleep(3)
    queue.enque(num*num)

t = threading.Thread(target = some_foo, args = (33, ))
t.start()
t.join()
print(queue.deque())